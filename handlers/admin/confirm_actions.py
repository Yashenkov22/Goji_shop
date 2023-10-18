from aiogram import types

from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import (add_category,
                        delete_category,
                        add_item,
                        delete_item,
                        update_item,
                        insert_photo,
                        delete_photo,
                        insert_artist,
                        delete_artist)


async def add_cat_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await add_category(session, data)
    except Exception as ex:
        print(ex)
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer(f'Категория {data["name"]} добавлена',
                                show_alert=True)
        

async def del_cat_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await delete_category(session, data)
    except Exception as ex:
        print(ex)
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer(f'Категория {data["category"]} удалена',
                                show_alert=True)
        

async def add_item_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await add_item(session, data)
    except Exception as ex:
        print(ex)
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer(f'Товар {data["name"]} добавлен',
                                show_alert=True)


async def del_item_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await delete_item(session, data['item_id'])
    except Exception as ex:
        print(ex)
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer(f'Товар {data["name"]} удален',
                                show_alert=True)
        

async def edit_item_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    new_data = {}
    old_item = data['old_item']
    new_data['id'] = old_item.id
    new_data['name'] = old_item.name if data['name'] == 'Нет' else data['name']
    new_data['price'] = old_item.price if data['price'] == 'Нет' else data['price']
    
    if old_item.name == new_data['name'] and int(old_item.price) == new_data['price']:
        await callback.answer('Товар остался таким же',
                                show_alert=True)
    else:
        try:
            await update_item(session, new_data)
        except Exception as ex:
            print(ex)
            await callback.answer('Не получилось',
                                    show_alert=True)
        else:
            await callback.answer('Товар изменён',
                                    show_alert=True)
            

async def add_photo_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await insert_photo(session, data)
    except Exception as ex:
        print(ex)
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer('Фото добавлен(о|ы)',
                                show_alert=True)
        

async def delete_photo_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await delete_photo(session, data)
    except Exception:
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer('Фото удалено',
                                show_alert=True)
        

async def add_artist_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await insert_artist(session, data)
    except Exception:
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer('Артист добавлен',
                                show_alert=True)
        

async def del_artist_action(callback: types.CallbackQuery,
                         session: AsyncSession,
                         data: dict):
    try:
        await delete_artist(session, data)
    except Exception:
        await callback.answer('Не получилось',
                                show_alert=True)
    else:
        await callback.answer('Артист удалён',
                                show_alert=True)


action_dict = {
    'add_cat': add_cat_action,
    'del_cat': del_cat_action,
    'add_item': add_item_action,
    'del_item': del_item_action,
    'edit_item': edit_item_action,
    'add_photo': add_photo_action,
    'delete_photo': delete_photo_action,
    'add_artist': add_artist_action,
    'del_artist': del_artist_action,
}