from decimal import Decimal, InvalidOperation

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

from .base import admin_page
from utils.callbacks import AddCategoryCallback
from utils.states import AdminItem
from db.queries import add_item


item_router = Router()

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
async def end_add_item(message: types.Message, state: FSMContext, session: Session):
    try:
        price = Decimal(message.text)
    except InvalidOperation:
        await message.answer('Цифрами напиши, голова')
        await process_add_item(message, state)
    else:
        await state.update_data(price=Decimal(message.text))
        data =  await state.get_data()
        try:
            add_item(session, data)
        except Exception as ex:
            print(ex)
            await message.answer('Не получилось')
        else:
            await message.answer(f'Товар {data["name"]} успешно добавлен')
        
        await state.clear()
        await admin_page(message)
