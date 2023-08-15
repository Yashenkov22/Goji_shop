from decimal import Decimal, InvalidOperation

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

from utils.states import AddItem, DeleteItem, EditItem
from utils.keyboards.admin_keyboards import create_confirm_kb
from utils.keyboards.shop_keyboards import create_category_kb, create_items_kb
from db.queries import select_current_item


item_router = Router()


#Add item
###############################################################################################
@item_router.message(F.text == 'Добавить товар')
async def add_item_to_db(message: types.Message, state: FSMContext, session: Session):
    await state.update_data(action='add_item')
    await state.set_state(AddItem.category)
    category_kb = create_category_kb(session, prefix='add_cat')
    await message.answer('Выбери категорию товара',
                         reply_markup=category_kb.as_markup())


@item_router.callback_query(F.data.startswith('add_cat'))
async def start_add_item(callback: types.CallbackQuery,
                         state: FSMContext):
    category = callback.data.split(':')[-1]
    await state.update_data(category=category)
    await state.set_state(AddItem.name)
    await callback.message.answer('Напиши название товара')
    await callback.message.delete()


@item_router.message(AddItem.name)
async def process_add_item(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not data.get('name'):
        await state.update_data(name=message.text.capitalize())

    await state.set_state(AddItem.price)
    await message.answer('Напиши цену товара')


@item_router.message(AddItem.price)
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
###############################################################################################


#Delete item
###############################################################################################
@item_router.message(F.text == 'Удалить товар')
async def del_item_from_db(message: types.Message, state: FSMContext, session: Session):
    await state.update_data(action='del_item')
    await state.set_state(DeleteItem.category)
    category_kb = create_category_kb(session, prefix='for_del_item')
    await message.answer('Выбери категорию товара',
                         reply_markup=category_kb.as_markup())


@item_router.callback_query(F.data.startswith('for_del_item'))
async def start_del_item(callback: types.CallbackQuery,
                         state: FSMContext,
                         session: Session):
    category = callback.data.split(':')[-1]
    await state.update_data(category=category)
    await state.set_state(DeleteItem.name)
    item_kb = create_items_kb(category, session, prefix='select_item_for_del')
    await callback.message.answer('Выбери товар, который хочешь удалить',
                                  reply_markup=item_kb.as_markup())
    await callback.message.delete()


@item_router.callback_query(F.data.startswith('select_item_for_del'))
async def start_del_item(callback: types.CallbackQuery,
                         state: FSMContext,
                         session: Session):
    name = callback.data.split(':')[-1]
    await state.update_data(name=name)
    data = await state.get_data()
    await callback.message.answer(f'Удалить товар {data["name"]} из категории {data["category"]}?',
                                  reply_markup=create_confirm_kb().as_markup())
    await callback.message.delete()
###############################################################################################


#Edit item
###############################################################################################
@item_router.message(F.text == 'Изменить товар')
async def edit_item_in_db(message: types.Message, state: FSMContext, session: Session):
    await state.update_data(action='edit_item')
    category_kb = create_category_kb(session, prefix='for_edit_item')
    await message.answer('Выбери категорию товара',
                         reply_markup=category_kb.as_markup())
    

@item_router.callback_query(F.data.startswith('for_edit_item'))
async def start_edit_item(callback: types.CallbackQuery,
                         state: FSMContext,
                         session: Session):
    category = callback.data.split(':')[-1]
    # await state.update_data(category=category)
    # await state.set_state(EditItem.name)
    item_kb = create_items_kb(category, session, prefix='select_item_for_edit')
    await callback.message.answer('Выбери товар, который хочешь изменить',
                                  reply_markup=item_kb.as_markup())
    await callback.message.delete()


@item_router.callback_query(F.data.startswith('select_item_for_edit'))
async def process_edit_item(callback: types.CallbackQuery,
                         state: FSMContext,
                         session: Session):
    name = callback.data.split(':')[-1]
    old_item = select_current_item(session, name)
    await state.update_data(old_item=old_item)
    print(old_item)
    await state.set_state(EditItem.name)
    await callback.message.answer(f'Напиши новое имя товара(Старое:{old_item[1]})\nЕсли не хочешь менять имя напиши Нет')
    await callback.message.delete()

@item_router.message(EditItem.name)
async def new_name_edit_item(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data.get('name'):
        await state.update_data(name=message.text.capitalize())
    old_price = round(data['old_item'][2], 2)
    await state.set_state(EditItem.price)
    await message.answer(f'Напиши новую цену товара(Старая:{old_price})\nЕсли не хочешь менять цену напиши Нет')


@item_router.message(EditItem.price)
async def new_price_edit_item(message: types.Message, state: FSMContext):
    if message.text.capitalize() == 'Нет':
        await state.update_data(price=message.text.capitalize())
    else:
        try:
            price = Decimal(message.text)
        except InvalidOperation:
            await message.answer('Цифрами напиши, голова')
            await new_name_edit_item(message, state)
        else:
            await state.update_data(price=int(price))
    
    data = await state.get_data()
    if data.get('price'):
        old_item = data['old_item']
        old_descr = f'Название:{old_item[1]}, Цена: {round(old_item[2])}'
        new_name = '(Не изменилось)' if data['name'] == 'Нет' else data['name']
        new_price = '(Не именилась)' if data['price'] == 'Нет' else data['price']
        new_descr = f'Название:{new_name}, Цена: {new_price}'
        await message.answer(f'Изменить товар {old_item[1]} из категории {old_item[-1]}?\nБыло: {old_descr}\nСтало: {new_descr}',
                            reply_markup=create_confirm_kb().as_markup())
###############################################################################################