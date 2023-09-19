from typing import Union
from random import choice

from aiogram import types, Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

# from handlers.admin.base import admin_page
from handlers.shop.base import show_categories, show_items_list
from config import PROMO_ID, PIC_IDS
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from utils.keyboards.main_keyboard import create_main_kb, create_close_kb
from utils.keyboards.shop_keyboards import create_shop_kb
from utils.keyboards.art_keyboards import create_art_kb


main_router = Router()

@main_router.message(Command('start'))
async def main_page(message: Union[types.Message, types.CallbackQuery],
                    state: FSMContext,
                    bot: Bot,
                    txt=None):
    if txt is None:
        await show_promo(message, bot, state)
    else:
        await try_delete_prev_message(bot, state)

        main_kb = create_main_kb(message.from_user.id)

        await state.update_data(prev_msg=list())
        data = await state.get_data()
        
        if isinstance(message, types.CallbackQuery):
            message = message.message
        
        photo = choice(PIC_IDS)

        msg = await message.answer_photo(photo,
                                         caption=txt,
                                         disable_notification=True,
                                         reply_markup=main_kb.as_markup(resize_keyboard=True,
                                                                        one_time_keyboard=True))

        add_message_for_delete(data, msg)
        
        try:
            await message.delete()
        except TelegramBadRequest:
             pass
        

async def show_promo(message: types.Message,
                     bot: Bot,
                     state: FSMContext):
    await message.answer_video(PROMO_ID,
                               disable_notification=True,
                               reply_markup=create_close_kb('promo').as_markup())
    
    await try_delete_prev_message(bot, state)
    
    await message.delete()


@main_router.message(F.text == 'Магазин')
async def to_shop(message: types.Message | types.CallbackQuery,
                  state: FSMContext,
                  bot: Bot):
    await try_delete_prev_message(bot, state)

    await state.update_data(prev_msg=list())
    data = await state.get_data()

    shop_kb = create_shop_kb()
    if isinstance(message, types.CallbackQuery):
        message = message.message

    msg = await message.answer('Goji Shop',
                               disable_notification=True,
                               reply_markup=shop_kb.as_markup(resize_keyboard=True))
    
    add_message_for_delete(data, msg)

    await message.delete()


@main_router.message(F.text == 'Творчество')
async def to_art(message: types.Message | types.CallbackQuery,
                 state: FSMContext,
                 bot: Bot):
    await try_delete_prev_message(bot, state)

    await state.update_data(prev_msg=list())
    data = await state.get_data()

    art_kb = create_art_kb()
    if isinstance(message, types.CallbackQuery):
        message = message.message

    msg = await message.answer('Goji Art',
                               disable_notification=True,
                               reply_markup=art_kb.as_markup(resize_keyboard=True))
    
    add_message_for_delete(data, msg)

    await message.delete()


@main_router.message(F.text == 'В главное меню')
async def show_link(message: types.Message,
                    bot: Bot,
                    state: FSMContext):
    await try_delete_prev_message(bot, state)

    await main_page(message,
                    state,
                    bot,
                    txt='Главное меню')
    
    # await message.delete()


@main_router.message(F.photo)
async def audio(message: types.Message):
    await message.answer(message.photo[0].file_id)


@main_router.callback_query(F.data.startswith('close'))
async def close_up(callback: types.CallbackQuery,
                   state: FSMContext,
                   bot: Bot):
    data = callback.data.split('_')[-1]
    if data == 'promo':
        await main_page(callback, state, bot, txt='Главное меню')
    else:
        await to_shop(callback.message,
                      state,
                      bot)


@main_router.callback_query(F.data.startswith('to'))
async def get_back_to(callback: types.CallbackQuery,
                      state: FSMContext,
                      bot: Bot,
                      session: AsyncSession,
                      **kwargs):
    if callback.data == 'to_main':
        await callback.answer('Вернул на главную')
        await to_shop(callback, state, bot)
    
    elif callback.data == 'to_categories':
        await callback.answer('Вернул на категории')
        await show_categories(callback.message,
                              state,
                              bot,
                              session)

    elif callback.data == 'to_items':
        data = await state.get_data()
        category = data['category']

        await state.clear()
        await callback.answer('Вернул к товарам')
        await show_items_list(callback,
                              state,
                              session,
                              cat=category)
        
    elif callback.data == 'to_art':
        await state.clear()
        await callback.answer('Вернул к творчеству')
        await to_art(callback,
                     state,
                     bot)
        
    elif callback.data == 'to_admin_page':
        await state.clear()
        await callback.answer('Вернул в админку')
        await main_page(callback,
                        state,
                        bot,
                        txt='Главное меню')


@main_router.message()
async def any_input(message: types.Message,
                    state: FSMContext,
                    bot: Bot):
    
    await main_page(message,
                    state,
                    bot,
                    txt='Не нужно сюда нечего писать, я интерактивный\nВыбери что нибудь из меню')