from typing import Union

from aiogram import Router, types, F
from aiogram.filters import Command

from sqlalchemy.orm.session import Session

from config import PROMO_ID
from utils.keyboards.shop_keyboards import (create_category_kb,
                                  create_items_kb,
                                  create_main_kb)
from utils.keyboards.promo_keyboards import close_kb


shop_router = Router()


@shop_router.message(Command('start'))
async def main_page(message: Union[types.Message, types.CallbackQuery],
                    txt='Главное меню'):
    main_kb = create_main_kb(message.from_user.id)
    
    if isinstance(message, types.CallbackQuery):
        message = message.message
    
    await message.answer(txt,
                        reply_markup=main_kb.as_markup(resize_keyboard=True,
                                                        one_time_keyboard=True))
    await message.delete()



@shop_router.message(F.text == 'Ассортимент')
async def show_categories(message: types.Message | types.CallbackQuery, session: Session):
    await message.answer('Выбери категорию',
                        reply_markup=create_category_kb(session).as_markup())
    await message.delete()


@shop_router.message(F.text == 'Промо')
async def show_promo(message: types.Message):
    await message.answer_video(PROMO_ID,
                               reply_markup=close_kb.as_markup())
    await message.delete()
    

@shop_router.message(F.text == 'Подробности')
async def show_promo(message: types.Message):
    await message.answer(f'Если возникли вопросы или предложения, пишите сюда https://t.me/dorriribka',
                         reply_markup=close_kb.as_markup())
    await message.delete()


@shop_router.callback_query(F.data.startswith('close'))
async def close_up(callback: types.CallbackQuery):
    await main_page(callback, txt='Закрыл')


@shop_router.callback_query(F.data.startswith('cat'))
async def show_items(callback: types.CallbackQuery,
                     session: Session):
    category = callback.data.split(':')[-1]
    item_kb = create_items_kb(category, session)
    await callback.message.delete()
    await callback.message.answer('Выбери товар',
                                  reply_markup=item_kb.as_markup())


@shop_router.callback_query()
async def get_back_to(callback: types.CallbackQuery, session: Session):
    if callback.data == 'to_main':
        await callback.answer('Вернул на главную')
        await main_page(callback)
    
    elif callback.data == 'to_categories':
        await callback.answer('Вернул на категории')
        await show_categories(callback.message, session)