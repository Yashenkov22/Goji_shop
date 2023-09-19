from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from utils.admin_decorator import admin_only
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from utils.cancel_admin_action import kb_with_cancel_btn
from utils.keyboards.admin_keyboards import create_confirm_kb
from utils.keyboards.art_keyboards import create_all_artists_kb
from utils.states import AddArtist, DelArtist


artist_router = Router()

#####################################ADD_ARTIST#############################################
@artist_router.message(F.text == 'Добавить артиста')
@admin_only
async def add_artist(message: types.Message,
                     state: FSMContext,
                     bot: Bot,
                     retry=None,
                     **kwargs):
    if retry is None:
        await try_delete_prev_message(bot, state)
        await state.update_data(action='add_artist')

        keyboard = kb_with_cancel_btn()

        artist_msg = await message.answer('Напиши название нового артиста\n<b>Максимальная длина 21 символ</b>',
                                    disable_notification=True,
                                    reply_markup=keyboard.as_markup(),
                                    parse_mode='html')
        
        await state.update_data(artist_msg=(artist_msg.chat.id, artist_msg.message_id))

        await message.delete()

    await state.set_state(AddArtist.name)


@artist_router.message(AddArtist.name)
@admin_only
async def start_add_artist(message: types.Message,
                         state: FSMContext,
                         bot: Bot,
                         **kwargs):
    data = await state.get_data()

    if data.get('artist_msg'):
        artist_msg = data['artist_msg']
        await bot.delete_message(*artist_msg)

    if len(message.text) > 21:
        await state.update_data(prev_msg=list())
        data = await state.get_data()
        
        msg = await message.answer('Я же написал, меньше 21го символа, придумай по короче',
                                   disable_notification=True)
        
        add_message_for_delete(data, msg)

        await add_artist(message,
                         state,
                         bot,
                         retry=True,
                         **kwargs)
    else:
        await state.update_data(name=message.text)

        await message.answer(f'Создать артиста <b>{message.text}</b>?',
                            disable_notification=True,
                            reply_markup=create_confirm_kb().as_markup(),
                            parse_mode='html')
        
        await message.delete()
############################################################################################


#####################################DELETE_ARTIST#############################################
@artist_router.message(F.text == 'Удалить артиста')
@admin_only
async def delete_artist(message: types.Message,
                        state: FSMContext,
                        session: AsyncSession,
                        bot: Bot,
                        **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='del_artist')
    await state.set_state(DelArtist.name)

    artist_kb = await create_all_artists_kb(session, prefix='del_artist')
    keyboard = kb_with_cancel_btn(keyboard=artist_kb)

    await message.answer('<b>Вместе с артистом удалятся все треки этого артиста!!!</b>\nВыбери артиста',
                        disable_notification=True,
                        reply_markup=keyboard.as_markup(),
                        parse_mode='html')
    
    await message.delete()


@artist_router.callback_query(F.data.startswith('del_artist'), DelArtist.name)
@admin_only
async def start_delete_artist(callback: types.CallbackQuery,
                              state: FSMContext,
                              session: AsyncSession,
                              bot: Bot,
                              **kwargs):
    artist_name = callback.data.split('_')[-1]

    await state.update_data(name=artist_name)

    await callback.message.answer(f'Удалить артиста <b>{artist_name}</b>?',
                                  disable_notification=True,
                                  reply_markup=create_confirm_kb().as_markup(),
                                  parse_mode='html')
    await callback.message.delete()