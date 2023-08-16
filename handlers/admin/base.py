from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session

from utils.keyboards.admin_keyboards import create_admin_kb
from db.queries import (add_category,
                        add_item,
                        delete_item,
                        update_item,
                        insert_photo)
from handlers.shop.base import main_page
from .admin_category import category_router
from .admin_item import item_router
from utils.admin_decorator import admin_only


admin_router = Router()
admin_router.include_router(category_router)
admin_router.include_router(item_router)


@admin_router.message(F.text == 'Админ панель')
@admin_only
async def admin_page(message: types.Message | types.CallbackQuery, **kwargs):
    admin_kb = create_admin_kb()
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer('Whazz`up, Жижа', reply_markup=admin_kb.as_markup(resize_keyboard=True,
                                                                        one_time_keyboard=True))


@admin_router.message(F.text == 'На главную')
@admin_only
async def create_category(message: types.Message, **kwargs):
    await main_page(message, txt='Главное меню')


@admin_router.callback_query(F.data.startswith('confirm'))
@admin_only
async def get_confirm(callback: types.CallbackQuery,
                      state: FSMContext,
                      session: Session,
                      **kwargs):
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
        
        elif data['action'] == 'add_item':
            try:
                add_item(session, data)
            except Exception as ex:
                print(ex)
                await callback.answer('Не получилось')
            else:
                await callback.answer(f'Товар {data["name"]} добавлен')

        elif data['action'] == 'del_item':
            try:
                delete_item(session, data)
            except Exception as ex:
                print(ex)
                await callback.answer('Не получилось')
            else:
                await callback.answer(f'Товар {data["name"]} удален')
        
        elif data['action'] == 'edit_item':
            new_data = {}
            old_item = data['old_item']
            new_data['id'] = old_item[0]
            new_data['name'] = old_item[1] if data['name'] == 'Нет' else data['name']
            new_data['price'] = old_item[2] if data['price'] == 'Нет' else data['price']
            if old_item[1] == new_data['name'] and int(old_item[2]) == new_data['price']:
                await callback.answer('Товар остался таким же')
            else:
                try:
                    update_item(session, new_data)
                except Exception as ex:
                    print(ex)
                    await callback.answer('Не получилось')
                else:
                    await callback.answer('Товар изменён')
        
        elif data['action'] == 'add_photo':
            try:
                insert_photo(session, data)
            except Exception as ex:
                print(ex)
                await callback.answer('Не получилось')
            else:
                await callback.answer('Фото добавлен(о|ы)')

    await state.clear()
    await callback.message.delete()
    await admin_page(callback)