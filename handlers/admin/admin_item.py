from decimal import Decimal, InvalidOperation

from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from utils.states import AddItem, DeleteItem, EditItem
from utils.keyboards.admin_keyboards import create_confirm_kb, load_photo_kb
from utils.keyboards.shop_keyboards import create_category_kb, create_items_kb
from utils.cancel_admin_action import kb_with_cancel_btn
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from utils.admin_decorator import admin_only
from db.queries import select_current_item


item_router = Router()

PHOTOS_FOR_LOAD = []


########################################Add item###############################################
@item_router.message(F.text == 'Добавить товар')
@admin_only
async def add_item_to_db(message: types.Message,
                         state: FSMContext,
                         bot: Bot,
                         session: AsyncSession,
                         **kwargs):
    await try_delete_prev_message(bot, state)
    
    await state.update_data(action='add_item')
    await state.set_state(AddItem.category)
    category_kb = await create_category_kb(session, prefix='add_item')
    keyboard = kb_with_cancel_btn(keyboard=category_kb)
    await message.answer('Выбери категорию товара',
                         reply_markup=keyboard.as_markup())
    await message.delete()


@item_router.callback_query(F.data.startswith('add_item'))
async def start_add_item(callback: types.CallbackQuery | types.Message,
                         state: FSMContext,
                         bot: Bot):
    data = await state.get_data()

    if not data.get('category'):
        category = callback.data.split(':')[-1]
        await state.update_data(category=category)
    
    await state.set_state(AddItem.name)
    
    if isinstance(callback, types.CallbackQuery):
        await state.update_data(prev_msg=list())
        data = await state.get_data()

        msg = await callback.message.answer('Напиши название товара\n<b>Максимальная длина - 21 символ</b>',
                                      parse_mode='html')
        
        add_message_for_delete(data, msg)

        await callback.message.delete()


@item_router.message(AddItem.name)
async def process_add_item(message: types.Message,
                           state: FSMContext,
                           bot: Bot):
    if len(message.text) > 21:
        data = await state.get_data()

        msg = await message.answer('Я же написал, меньше 21го символа, придумай по короче')

        await start_add_item(message, state)
    else:
        data = await state.get_data()

        if not data.get('name'):
            await state.update_data(name=message.text.capitalize())

        await state.set_state(AddItem.price)
        msg = await message.answer('Напиши цену товара')
        
        await message.delete()
    
    add_message_for_delete(data, msg)


@item_router.message(AddItem.price)
async def end_add_item(message: types.Message,
                       state: FSMContext,
                       bot: Bot):
    try:
        price = Decimal(message.text)
    except InvalidOperation:
        data = await state.get_data()

        msg = await message.answer('Цифрами напиши, голова')
        add_message_for_delete(data, msg)
        
        await process_add_item(message, state, bot)
    else:
        await state.update_data(price=price)
        data = await state.get_data()
        await message.answer(f'Создать товар <b>{data["name"].capitalize()}</b> в категории <b>{data["category"]}</b>?',
                             reply_markup=create_confirm_kb().as_markup(),
                             parse_mode='html')
        await message.delete()
###############################################################################################



######################################Delete item##############################################
@item_router.message(F.text == 'Удалить товар')
@admin_only
async def del_item_from_db(message: types.Message,
                           state: FSMContext,
                           bot: Bot,
                           session: AsyncSession,
                           **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='del_item')
    await state.set_state(DeleteItem.category)

    category_kb = await create_category_kb(session, prefix='for_del_item')
    keyboard = kb_with_cancel_btn(keyboard=category_kb)
    await message.answer('<b>Вместе с товаром удалятся все фото этого товара!!!</b>\nВыбери категорию товара',
                         reply_markup=keyboard.as_markup(),
                         parse_mode='html')
    await message.delete()


@item_router.callback_query(F.data.startswith('for_del_item'))
async def start_del_item(callback: types.CallbackQuery,
                         state: FSMContext,
                         session: AsyncSession):
    category = callback.data.split(':')[-1]
    await state.update_data(category=category)
    await state.set_state(DeleteItem.name)
    item_kb = await create_items_kb(category, session, prefix='select_item_for_del')

    if item_kb is None:
        await callback.answer('В категории нет товаров')
    else:
        await callback.message.answer('Выбери товар, который хочешь удалить',
                                    reply_markup=item_kb.as_markup())
        await callback.message.delete()


@item_router.callback_query(F.data.startswith('select_item_for_del'))
async def start_del_item(callback: types.CallbackQuery,
                         session: AsyncSession,
                         state: FSMContext):
    name = callback.data.split(':')[-1]
    await state.update_data(name=name)
    item = await select_current_item(session, name)
    item_id = item[0].id
    await state.update_data(item_id=item_id)
    data = await state.get_data()
    await callback.message.answer(f'Удалить товар <b>{name}</b> из категории <b>{data["category"]}</b>?',
                                  reply_markup=create_confirm_kb().as_markup(),
                                  parse_mode='html')
    await callback.message.delete()
###############################################################################################


########################################Edit item##############################################
@item_router.message(F.text == 'Изменить товар')
@admin_only
async def edit_item_in_db(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          session: AsyncSession,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='edit_item')
    category_kb = await create_category_kb(session, prefix='for_edit_item')
    keyboard = kb_with_cancel_btn(keyboard=category_kb)
    await message.answer('Выбери категорию товара',
                         reply_markup=keyboard.as_markup())
    await message.delete()
    

@item_router.callback_query(F.data.startswith('for_edit_item'))
async def start_edit_item(callback: types.CallbackQuery,
                          session: AsyncSession):
    category = callback.data.split(':')[-1]
    item_kb = await create_items_kb(category, session, prefix='select_item_for_edit')
    if item_kb is None:
        await callback.answer('В категории нет товаров')
    else:
        await callback.message.answer('Выбери товар, который хочешь изменить',
                                    reply_markup=item_kb.as_markup())
        await callback.message.delete()


@item_router.callback_query(F.data.startswith('select_item_for_edit'))
async def process_edit_item(callback: types.CallbackQuery,
                            state: FSMContext,
                            bot: Bot,
                            session: AsyncSession):
    name = callback.data.split(':')[-1]

    old_item = await select_current_item(session, name)
    old_item = old_item[0]
    await state.update_data(old_item=old_item)
    
    await state.set_state(EditItem.name)

    await state.update_data(prev_msg=list())
    data = await state.get_data()

    msg = await callback.message.answer(f'Напиши новое имя товара(Старое: <b>{old_item.name}</b>)\nЕсли не хочешь менять имя напиши <b>Нет</b>',
                                  parse_mode='html')
    
    add_message_for_delete(data, msg)

    await callback.message.delete()


@item_router.message(EditItem.name)
async def new_name_edit_item(message: types.Message,
                             state: FSMContext,
                             bot: Bot):
    data = await state.get_data()

    if not data.get('name'):
        await state.update_data(name=message.text.capitalize())

    old_price = round(data['old_item'].price, 2)
    await state.set_state(EditItem.price)

    msg = await message.answer(f'Напиши новую цену товара(Старая: <b>{old_price}</b>)\nЕсли не хочешь менять цену напиши <b>Нет</b>',
                         parse_mode='html')
    
    add_message_for_delete(data, msg)

    await message.delete()


@item_router.message(EditItem.price)
async def new_price_edit_item(message: types.Message,
                              state: FSMContext,
                              bot: Bot):
    if message.text.capitalize() == 'Нет':
        await state.update_data(price=message.text.capitalize())
    else:
        try:
            price = Decimal(message.text)
        except InvalidOperation:
            data = await state.get_data()

            msg = await message.answer('Цифрами напиши, голова')
            add_message_for_delete(data, msg)

            await new_name_edit_item(message, state, bot)
        else:
            await state.update_data(price=int(price))
    
    data = await state.get_data()

    if data.get('price'):
        old_item = data['old_item']
        old_descr = f'Название: {old_item.name}, Цена: {round(old_item.price)}'
        new_name = '(Не изменилось)' if data['name'] == 'Нет' else data['name']
        new_price = '(Не именилась)' if data['price'] == 'Нет' else data['price']
        new_descr = f'Название: {new_name}, Цена: {new_price}'
        await message.answer(f'Изменить товар <b>{old_item.name}</b> из категории <b>{old_item.category}</b>?\nБыло: {old_descr}\nСтало: {new_descr}',
                             reply_markup=create_confirm_kb().as_markup(),
                             parse_mode='html')
        await message.delete()
###############################################################################################


########################################Add photo###############################################
@item_router.message(F.text == 'Добавить фото к товару')
@admin_only
async def add_photo_to_item(message: types.Message,
                            state: FSMContext,
                            bot: Bot,
                            session: AsyncSession,
                            **kwargs):
    await try_delete_prev_message(bot, state)

    await state.update_data(action='add_photo')
    category_kb = await create_category_kb(session, prefix='add_photo')
    keyboard = kb_with_cancel_btn(keyboard=category_kb)
    await message.answer('Выбери категорию товара',
                         reply_markup=keyboard.as_markup())
    
    await message.delete()
    

@item_router.callback_query(F.data.startswith('add_photo'))
async def start_add_photo(callback: types.CallbackQuery,
                          session: AsyncSession):
    category = callback.data.split(':')[-1]
    item_kb = await create_items_kb(category, session, prefix='item_for_add_photo')
    if item_kb is None:
        await callback.answer('В категории нет товаров')
    else:
        await callback.message.answer('Выбери товар, к которому добавить фото',
                                    reply_markup=item_kb.as_markup())
        await callback.message.delete()


@item_router.callback_query(F.data.startswith('item_for_add_photo'))
async def process_add_photo(callback: types.CallbackQuery,
                          state: FSMContext,
                          bot: Bot,
                          session: AsyncSession):
    item_name = callback.data.split(':')[-1]
    item = await select_current_item(session, item_name)
    await state.update_data(item_id=item[0].id, item_name=item_name)

    await state.update_data(prev_msg=list())
    data = await state.get_data()

    msg = await callback.message.answer('Загрузи и отправь фото (<b>можно сразу несколько</b>)',
                                  parse_mode='html')

    add_message_for_delete(data, msg)

    await callback.message.delete()

@item_router.message(F.photo)
@admin_only
async def load_photo(message: types.Message,
                     state: FSMContext,
                     bot: Bot,
                     **kwargs):
    photo_id = message.photo[0].file_id
    PHOTOS_FOR_LOAD.append(photo_id)

    data = await state.get_data()

    msg = await message.answer(f'Фото обработано',
                         reply_markup=load_photo_kb().as_markup(resize_keyboard=True))
    
    add_message_for_delete(data, msg)

    await message.delete()


@item_router.message(F.text == 'Продолжить')
@admin_only
async def add_photo_in_state(message: types.Message,
                             state: FSMContext,
                             **kwargs):
    global PHOTOS_FOR_LOAD

    await state.update_data(photos=PHOTOS_FOR_LOAD)
    data = await state.get_data()
    PHOTOS_FOR_LOAD = []
    await message.answer(f'Добавить фото к товару <b>{data["item_name"]}</b>?',
                         reply_markup=create_confirm_kb().as_markup(),
                         parse_mode='html')
    await message.delete()
###############################################################################################