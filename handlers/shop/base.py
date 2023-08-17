from typing import Union

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm.session import Session

from config import PROMO_ID
from utils.keyboards.shop_keyboards import (create_category_kb,
                                            create_items_kb,
                                            create_main_kb,
                                            create_close_kb)
from .shop_item import item_view_router


shop_router = Router()
shop_router.include_router(item_view_router)


@shop_router.message(Command('start'))
async def main_page(message: Union[types.Message, types.CallbackQuery],
                    txt=None):
    if txt is None:
        await show_promo(message)
    else:
        main_kb = create_main_kb(message.from_user.id)
        
        if isinstance(message, types.CallbackQuery):
            message = message.message
        
        await message.answer(txt,
                            reply_markup=main_kb.as_markup(resize_keyboard=True,
                                                           one_time_keyboard=True))
        await message.delete()


@shop_router.message(F.text == 'Ассортимент')
async def show_categories(message: types.Message | types.CallbackQuery,
                          session: Session):
    await message.answer('Выбери категорию',
                         reply_markup=create_category_kb(session).as_markup())
    await message.delete()


@shop_router.message(F.text == 'Промо')
async def show_promo(message: types.Message):
    await message.answer_video(PROMO_ID,
                               reply_markup=create_close_kb().as_markup())
    await message.delete()
    

@shop_router.message(F.text == 'Подробности')
async def show_link(message: types.Message):
    await message.answer(f'Если возникли вопросы или предложения, пишите сюда https://t.me/dorriribka',
                         reply_markup=create_close_kb().as_markup())
    await message.delete()


#Close button callback handler
@shop_router.callback_query(F.data.startswith('close'))
async def close_up(callback: types.CallbackQuery):
    await main_page(callback, txt='Главное меню')


#Category button callback handler
@shop_router.callback_query(F.data.startswith('cat'))
async def show_items_list(callback: types.CallbackQuery,
                          state: FSMContext,
                          session: Session,
                          cat: str = None):
    category = callback.data.split(':')[-1] if cat is None else cat
    await state.update_data(category=category)
    item_kb = create_items_kb(category, session)
    
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
                      session: Session):
    if callback.data == 'to_main':
        await callback.answer('Вернул на главную')
        await main_page(callback, txt='Главное меню')
    
    elif callback.data == 'to_categories':
        await callback.answer('Вернул на категории')
        await show_categories(callback.message, session)

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
async def any_input(message: types.Message):
    await message.answer('Не нужно сюда нечего писать, я интерактивный')
    await main_page(message, txt='Выбери что нибудь из меню')

