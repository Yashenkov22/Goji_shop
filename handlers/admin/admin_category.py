from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from utils.states import AddCategory, DeleteCategory
from utils.keyboards.admin_keyboards import create_confirm_kb
from utils.keyboards.shop_keyboards import create_category_kb
from utils.admin_decorator import admin_only
from utils.cancel_admin_action import kb_with_cancel_btn
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)


category_router = Router()

@category_router.message(F.text == 'Добавить категорию')
@admin_only
async def create_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='add_cat')
    await state.set_state(AddCategory.name)

    keyboard = kb_with_cancel_btn()
    
    cat_msg = await message.answer('Напиши название новой категории\n<b>Максимальная длина 21 символ</b>',
                                   disable_notification=True,
                                   reply_markup=keyboard.as_markup(),
                                   parse_mode='html')
    
    await state.update_data(cat_msg=(cat_msg.chat.id, cat_msg.message_id))

    await message.delete()


@category_router.message(AddCategory.name)
@admin_only
async def start_category(message: types.Message,
                         state: FSMContext,
                         bot: Bot,
                         **kwargs):
    data = await state.get_data()

    if data.get('cat_msg'):
        cat_msg = data['cat_msg']
        await bot.delete_message(*cat_msg)

    await state.update_data(name=message.text.capitalize())

    await message.answer(f'Создать категорию <b>{message.text.capitalize()}</b>?',
                         disable_notification=True,
                         reply_markup=create_confirm_kb().as_markup(),
                         parse_mode='html')
    
    await message.delete()


@category_router.message(F.text == 'Удалить категорию')
@admin_only
async def delete_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          session: AsyncSession,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='del_cat')
    category_list = await create_category_kb(session, prefix='del_cat')
    
    await state.set_state(DeleteCategory.category)
    keyboard = kb_with_cancel_btn(category_list)

    await message.answer('<b>Все товары, связанные с выбранной категорией, будут удалены вместе с ней</b>\nВыбери категорию для удаления',
                         disable_notification=True,
                         reply_markup=keyboard.as_markup(),
                         parse_mode='html')
    
    await message.delete()


@category_router.callback_query(F.data.startswith('del_cat'))
@admin_only
async def delete_category(callback: types.CallbackQuery,
                          state: FSMContext,
                          **kwargs):
    category = callback.data.split(':')[-1]
    await state.update_data(category=category)

    await callback.message.answer(f'Удалить категорию <b>{category}</b>?',
                                  disable_notification=True,
                                  reply_markup=create_confirm_kb().as_markup(),
                                  parse_mode='html')
    await callback.message.delete()
