from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from utils.keyboards.admin_keyboards import (create_admin_kb,
                                             create_manage_category_kb,
                                             create_manage_item_kb,
                                             create_manage_photo_kb,
                                             create_to_abmin_page_kb,
                                             create_manage_artist_kb)
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from utils.admin_decorator import admin_only
from db.queries import (add_category,
                        delete_category,
                        add_item,
                        delete_item,
                        update_item,
                        insert_photo,
                        delete_photo,
                        insert_artist,
                        delete_artist)
from handlers.base import main_page
from .admin_category import category_router
from .admin_item import item_router
from .admin_artist import artist_router
from .confirm_actions import action_dict

admin_router = Router()
admin_router.include_router(category_router)
admin_router.include_router(item_router)
admin_router.include_router(artist_router)


@admin_router.message(F.text == 'Админ панель')
@admin_only
async def admin_page(message: types.Message | types.CallbackQuery,
                     state: FSMContext,
                     bot: Bot,
                     **kwargs):
    await try_delete_prev_message(bot, state)

    admin_kb = create_admin_kb()
    
    if isinstance(message, types.CallbackQuery):
        message = message.message
    
    msg = await message.answer('Whazz`up, Жижа',
                               disable_notification=True,
                               reply_markup=admin_kb.as_markup(resize_keyboard=True,
                                                               one_time_keyboard=True))

    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    try:    
        await message.delete()
    except TelegramBadRequest:
        pass


@admin_router.message(F.text == 'Управление категориями')
@admin_only
async def manage_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    manage_cat_kb = create_manage_category_kb()

    keyboard = create_to_abmin_page_kb(manage_cat_kb)

    msg = await message.answer('Выбери действие',
                               disable_notification=True,
                               reply_markup=keyboard.as_markup(resize_keyboard=True))
    
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    await message.delete()


@admin_router.message(F.text == 'Управление товарами')
@admin_only
async def manage_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    manage_item_kb = create_manage_item_kb()

    keyboard = create_to_abmin_page_kb(manage_item_kb)

    msg = await message.answer('Выбери действие',
                               disable_notification=True,
                               reply_markup=keyboard.as_markup(resize_keyboard=True))
    
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    await message.delete()


@admin_router.message(F.text == 'Управление фото')
@admin_only
async def manage_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    manage_photo_kb = create_manage_photo_kb()

    keyboard = create_to_abmin_page_kb(manage_photo_kb)

    msg = await message.answer('Выбери действие',
                               disable_notification=True,
                               reply_markup=keyboard.as_markup(resize_keyboard=True))
    
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    await message.delete()


@admin_router.message(F.text == 'Управление артистами')
@admin_only
async def manage_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    manage_artist_kb = create_manage_artist_kb()

    keyboard = create_to_abmin_page_kb(manage_artist_kb)

    msg = await message.answer('Выбери действие',
                               disable_notification=True,
                               reply_markup=keyboard.as_markup(resize_keyboard=True))
    
    await state.update_data(prev_msg=list())
    data = await state.get_data()

    add_message_for_delete(data, msg)

    await message.delete()


@admin_router.message(F.text == 'Назад в админ панель')
@admin_only
async def  back_to_admin_page(message: types.Message,
                              state: FSMContext,
                              bot: Bot,
                              **kwargs):
    await admin_page(message, state, bot, **kwargs)

    # await message.delete()


@admin_router.message(F.text == 'На главную')
@admin_only
async def create_category(message: types.Message,
                          state: FSMContext,
                          bot: Bot,
                          **kwargs):
    await try_delete_prev_message(bot, state)

    await main_page(message, state, bot, txt='Главное меню')


@admin_router.callback_query(F.data.startswith('confirm'))
@admin_only
async def get_confirm(callback: types.CallbackQuery,
                      state: FSMContext,
                      bot: Bot,
                      session: AsyncSession,
                      **kwargs):
    confirm = callback.data.split(':')[-1]

    if confirm == 'no':
        await callback.answer('Ну ты и Буба волосатая')
    
    else:
        data = await state.get_data()

        action_func = action_dict[data['action']]

        await action_func(callback, session, data)


        
        # if data['action'] == 'add_cat':
        #     try:
        #         await add_category(session, data)
        #     except Exception as ex:
        #         print(ex)
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer(f'Категория {data["name"]} добавлена',
        #                               show_alert=True)

        # elif data['action'] == 'del_cat':
        #     try:
        #         await delete_category(session, data)
        #     except Exception as ex:
        #         print(ex)
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer(f'Категория {data["category"]} удалена',
        #                               show_alert=True)
        
        # elif data['action'] == 'add_item':
        #     try:
        #         await add_item(session, data)
        #     except Exception as ex:
        #         print(ex)
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer(f'Товар {data["name"]} добавлен',
        #                               show_alert=True)
            

        # elif data['action'] == 'del_item':
        #     try:
        #         await delete_item(session, data['item_id'])
        #     except Exception as ex:
        #         print(ex)
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer(f'Товар {data["name"]} удален',
        #                               show_alert=True)
        
        # elif data['action'] == 'edit_item':
        #     new_data = {}
        #     old_item = data['old_item']
        #     new_data['id'] = old_item.id
        #     new_data['name'] = old_item.name if data['name'] == 'Нет' else data['name']
        #     new_data['price'] = old_item.price if data['price'] == 'Нет' else data['price']
            
        #     if old_item.name == new_data['name'] and int(old_item.price) == new_data['price']:
        #         await callback.answer('Товар остался таким же',
        #                               show_alert=True)
        #     else:
        #         try:
        #             await update_item(session, new_data)
        #         except Exception as ex:
        #             print(ex)
        #             await callback.answer('Не получилось',
        #                                   show_alert=True)
        #         else:
        #             await callback.answer('Товар изменён',
        #                                   show_alert=True)
        
        # elif data['action'] == 'add_photo':
        #     try:
        #         await insert_photo(session, data)
        #     except Exception as ex:
        #         print(ex)
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer('Фото добавлен(о|ы)',
        #                               show_alert=True)

        # elif data['action'] == 'delete_photo':
        #     try:
        #         await delete_photo(session, data)
        #     except Exception:
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer('Фото удалено',
        #                               show_alert=True)

        # elif data['action'] == 'add_artist':
        #     try:
        #         await insert_artist(session, data)
        #     except Exception:
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer('Артист добавлен',
        #                               show_alert=True)

        # elif data['action'] == 'del_artist':
        #     try:
        #         await delete_artist(session, data)
        #     except Exception:
        #         await callback.answer('Не получилось',
        #                               show_alert=True)
        #     else:
        #         await callback.answer('Артист удалён',
        #                               show_alert=True)

    await try_delete_prev_message(bot, state)

    await state.clear()
    await admin_page(callback, state, bot, **kwargs)
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass