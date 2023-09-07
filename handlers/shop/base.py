from typing import Union

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from config import PROMO_ID
from utils.keyboards.shop_keyboards import (create_category_kb,
                                            create_items_kb,
                                            create_main_kb,
                                            create_close_kb)
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from .shop_item import item_view_router


shop_router = Router()
shop_router.include_router(item_view_router)


@shop_router.message(Command('start'))
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
        
        msg = await message.answer(txt,
                                   reply_markup=main_kb.as_markup(resize_keyboard=True,
                                                                  one_time_keyboard=True))

        add_message_for_delete(data, msg)
        
        try:
            await message.delete()
        except TelegramBadRequest:
             pass

@shop_router.message(F.text == 'Ассортимент')
async def show_categories(message: types.Message | types.CallbackQuery,
                          state: FSMContext,
                          bot: Bot,
                          session: AsyncSession):
    await try_delete_prev_message(bot, state)

    category_kb = await create_category_kb(session)
    await message.answer('Выбери категорию',
                         reply_markup=category_kb.as_markup())
    
    await message.delete()


@shop_router.message(F.text == 'Промо')
async def show_promo(message: types.Message,
                     bot: Bot,
                     state: FSMContext):
    await message.answer_video(PROMO_ID,
                               reply_markup=create_close_kb().as_markup())
    
    await try_delete_prev_message(bot, state)
    
    await message.delete()
    

@shop_router.message(F.text == 'Написать продавцу')
async def show_link(message: types.Message,
                    bot: Bot,
                    state: FSMContext):
    await try_delete_prev_message(bot, state)

    await message.answer(f'Если возникли вопросы или предложения, пишите сюда https://t.me/dorriribka',
                         reply_markup=create_close_kb().as_markup())
    
    await message.delete()


#Close button callback handler
@shop_router.callback_query(F.data.startswith('close'))
async def close_up(callback: types.CallbackQuery,
                   state: FSMContext,
                   bot: Bot):
    await main_page(callback, state, bot, txt='Главное меню')


#Category button callback handler
@shop_router.callback_query(F.data.startswith('cat'))
async def show_items_list(callback: types.CallbackQuery,
                          state: FSMContext,
                          session: AsyncSession,
                          cat: str = None):
    category = callback.data.split(':')[-1] if cat is None else cat
    await state.update_data(category=category)
    item_kb = await create_items_kb(category, session)
    
    if item_kb is None:
        await callback.answer('В категории пока нет товаров',
                              show_alert=True)
    else:
        await callback.message.answer('Выбери товар',
                                    reply_markup=item_kb.as_markup())
        await callback.message.delete()


#To back button callback handler
@shop_router.callback_query(F.data.startswith('to'))
async def get_back_to(callback: types.CallbackQuery,
                      state: FSMContext,
                      bot: Bot,
                      session: AsyncSession):
    if callback.data == 'to_main':
        await callback.answer('Вернул на главную')
        await main_page(callback, state, bot, txt='Главное меню')
    
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


#Any input handler
@shop_router.message()
async def any_input(message: types.Message, state: FSMContext):
    await message.answer('Не нужно сюда нечего писать, я интерактивный')
    await main_page(message, state, txt='Выбери что нибудь из меню')

