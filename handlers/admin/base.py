from decimal import Decimal, InvalidOperation

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

from utils.keyboards.admin_keyboards import (create_admin_kb,
                                             create_confirm_kb,
                                             category_list_for_add)
from utils.callbacks import AddCategoryCallback
from utils.states import AdminCategory, AdminItem
from db.queries import add_category, add_item
from handlers.shop import main_page
from .add_category import category_router
from .add_item import item_router


admin_router = Router()
admin_router.include_router(category_router)
admin_router.include_router(item_router)


@admin_router.message(F.text == 'Админ панель')
async def admin_page(message: types.Message | types.CallbackQuery):
    admin_kb = create_admin_kb()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer('Здорова, Сало', reply_markup=admin_kb.as_markup(resize_keyboard=True,
                                                                        one_time_keyboard=True))

# @admin_router.message(F.text == 'Добавить категорию')
# async def create_category(message: types.Message, state: FSMContext):
#     await state.update_data(action='add_cat')
#     await state.set_state(AdminCategory.name)
#     await message.answer('Напиши название новой категории')


# @admin_router.message(AdminCategory.name)
# async def start_category(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text.capitalize())
#     await message.answer(f'Создать категорию {message.text.capitalize()}?',
#                          reply_markup=create_confirm_kb().as_markup())
    

@admin_router.callback_query(F.data.startswith('confirm'))
async def get_confirm(callback: types.CallbackQuery,
                      state: FSMContext,
                      session: Session):
    confirm = callback.data.split(':')[-1]

    if confirm == 'no':
        await callback.answer('Ну ты и Буба волосатая')
    else:
        data = await state.get_data()
        
        if data['action'] == 'add_cat':
            try:
                add_category(session, data)
            except Exception as ex:
                print(ex)
                await callback.answer('Не получилось')
            else:
                await callback.answer(f'Категория {data["name"]} добавлена')
    await state.clear()
    await callback.message.delete()
    await admin_page(callback)


@admin_router.message(F.text == 'Добавить товар')
async def add_item_to_db(message: types.Message, state: FSMContext, session: Session):
    await state.set_state(AdminItem.category)
    category_kb = category_list_for_add(session)
    await message.answer('Выбери категорию товара',
                         reply_markup=category_kb.as_markup())
    

# @admin_router.callback_query(AddCategoryCallback.filter(F.prefix == 'add_cat'))
# async def start_add_item(callback: types.CallbackQuery,
#                    callback_data: AddCategoryCallback,
#                    state: FSMContext):
#     category = callback_data.category
#     await state.update_data(category=category)
#     await state.set_state(AdminItem.name)
#     await callback.message.answer('Напиши название товара')
#     await callback.message.delete()


# @admin_router.message(AdminItem.name)
# async def process_add_item(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     if not data.get('name'):
#         await state.update_data(name=message.text.capitalize())
#     await state.set_state(AdminItem.price)
#     await message.answer('Напиши цену товара')


# @admin_router.message(AdminItem.price)
# async def end_add_item(message: types.Message, state: FSMContext, session: Session):
#     try:
#         price = Decimal(message.text)
#     except InvalidOperation:
#         await message.answer('Цифрами напиши, голова')
#         await process_add_item(message, state)
#     else:
#         await state.update_data(price=Decimal(message.text))
#         data =  await state.get_data()
#         try:
#             add_item(session, data)
#         except Exception as ex:
#             print(ex)
#             await message.answer('Не получилось')
#         else:
#             await message.answer(f'Товар {data["name"]} успешно добавлен')
        
#         await state.clear()
#         await admin_page(message)



@admin_router.message(F.text == 'На главную')
async def create_category(message: types.Message):
    await main_page(message)