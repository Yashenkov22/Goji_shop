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
from utils.item_photo import item_constructor
from db.queries import select_current_item, select_photos_for_item


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
async def show_promo(message: types.Message):
    await message.answer(f'Если возникли вопросы или предложения, пишите сюда https://t.me/dorriribka',
                         reply_markup=create_close_kb().as_markup())
    await message.delete()


#Close button callback handler
@shop_router.callback_query(F.data.startswith('close'))
async def close_up(callback: types.CallbackQuery):
    await main_page(callback, txt='Закрыл')


#Category button callback handler
@shop_router.callback_query(F.data.startswith('cat'))
async def show_items_list(callback: types.CallbackQuery,
                     state: FSMContext,
                     session: Session,
                     cat: str = None):
    category = callback.data.split(':')[-1] if cat is None else cat
    await state.update_data(category=category)
    item_kb = create_items_kb(category, session)
    await callback.message.delete()
    await callback.message.answer('Выбери товар',
                                  reply_markup=item_kb.as_markup())


###################################Show_item###############################################
@shop_router.callback_query(F.data.startswith('show_item'))
async def init_current_item(callback: types.CallbackQuery,
                            state: FSMContext,
                            session: Session):
    item_name = callback.data.split(':')[-1]
    item = select_current_item(session, item_name)
    item_id = item[0]
    item_photos = list(map(lambda photo: photo[0],select_photos_for_item(session, item_id)))
    await state.update_data(name=item[1])
    await state.update_data(price=item[2])
    await state.update_data(photos=item_photos)
    await state.update_data(photo_idx=0)
    
    await show_item(callback, state)
    await callback.message.delete()


async def show_item(callback: types.CallbackQuery,
                    state: FSMContext):
    data = await state.get_data()
    name, price, photo, photo_kb = item_constructor(data)
    await callback.message.answer_photo(photo,
                            caption=f'Товар: {name}\nЦена: {price}',
                            reply_markup=photo_kb.as_markup())


async def switch_item_photo(callback: types.CallbackQuery,
                            state: FSMContext):
    data = await state.get_data()
    name, price, photo, photo_kb = item_constructor(data)
    
    await callback.message.edit_media(types.InputMediaPhoto(media=photo,
                                                        type='photo'),
                                        caption=f'Товар: {name}\nЦена: {price}',
                                        reply_markup=photo_kb.as_markup())


@shop_router.callback_query(F.data.startswith('photo'))
async def init_current_item(callback: types.CallbackQuery,
                            state: FSMContext):
    action = callback.data.split('_')[-1]
    data = await state.get_data()
    photo_idx = data['photo_idx']
    match action:
        case 'next':
            await state.update_data(photo_idx=photo_idx+1)
        case 'prev':
            await state.update_data(photo_idx=photo_idx-1)
    await switch_item_photo(callback, state)

###################################################################################

#To back button callback handler
@shop_router.callback_query()
async def get_back_to(callback: types.CallbackQuery,
                      state: FSMContext,
                      session: Session):
    if callback.data == 'to_main':
        await callback.answer('Вернул на главную')
        await main_page(callback)
    
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

