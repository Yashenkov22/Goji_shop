from decimal import Decimal, InvalidOperation

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

from utils.callbacks import AddCategoryCallback
from utils.states import AdminItem
from utils.keyboards.admin_keyboards import category_list_for_add, create_confirm_kb


item_router = Router()


@item_router.message(F.text == 'Добавить товар')
async def add_item_to_db(message: types.Message, state: FSMContext, session: Session):
    await state.update_data(action='add_item')
    await state.set_state(AdminItem.category)
    category_kb = category_list_for_add(session)
    await message.answer('Выбери категорию товара',
                         reply_markup=category_kb.as_markup())


@item_router.callback_query(AddCategoryCallback.filter(F.prefix == 'add_cat'))
async def start_add_item(callback: types.CallbackQuery,
                         callback_data: AddCategoryCallback,
                         state: FSMContext):
    category = callback_data.category
    await state.update_data(category=category)
    await state.set_state(AdminItem.name)
    await callback.message.answer('Напиши название товара')
    await callback.message.delete()


@item_router.message(AdminItem.name)
async def process_add_item(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not data.get('name'):
        await state.update_data(name=message.text.capitalize())

    await state.set_state(AdminItem.price)
    await message.answer('Напиши цену товара')


@item_router.message(AdminItem.price)
async def end_add_item(message: types.Message, state: FSMContext):
    try:
        price = Decimal(message.text)
    except InvalidOperation:
        await message.answer('Цифрами напиши, голова')
        await process_add_item(message, state)
    else:
        await state.update_data(price=price)
        data = await state.get_data()
        await message.answer(f'Создать товар {data["name"].capitalize()}?',
                                reply_markup=create_confirm_kb().as_markup())