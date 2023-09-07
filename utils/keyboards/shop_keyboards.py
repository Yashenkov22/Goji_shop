from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from utils.callbacks import CloseCallback
from db.queries import get_all_categories, get_items_for_current_category
from config import ADMIN_IDS


#Keyboard on main page
def create_main_kb(user_id):

    main_kb = ReplyKeyboardBuilder()
    main_kb.row(types.KeyboardButton(text='Ассортимент'))
    main_kb.row(types.KeyboardButton(text='Промо'))
    main_kb.row(types.KeyboardButton(text='Написать продавцу'))
    if user_id in ADMIN_IDS:
        main_kb.row(types.KeyboardButton(text='Админ панель'))
    return main_kb

#Inline keyboard categories
async def create_category_kb(session: AsyncSession, prefix: str = 'cat') -> InlineKeyboardBuilder:
    category_list = await get_all_categories(session)
    category_kb = InlineKeyboardBuilder()
    for cat in category_list:
        category_kb.row(
            types.InlineKeyboardButton(text=cat[0],
                                       callback_data=f'{prefix}:{cat[0]}')
        )
    if prefix == 'cat':
        category_kb.row(types.InlineKeyboardButton(text='Назад',
                                                callback_data='to_main'))
    return category_kb


#Inline keyboard items
async def create_items_kb(category: str,
                    session: AsyncSession,
                    prefix: str = 'show_item') -> InlineKeyboardBuilder:
    item_list = await get_items_for_current_category(category, session)
    
    if not item_list:
        return 

    item_kb = InlineKeyboardBuilder()
    for item in item_list:
        item_kb.row(types.InlineKeyboardButton(text=item[0].name,
                                               callback_data=f'{prefix}:{item[0].name}'))
    if prefix == 'show_item':
        item_kb.row(types.InlineKeyboardButton(text='Назад',
                                            callback_data='to_categories'))
    return item_kb


#Inline photo keyboard
def create_photo_keyboard(kb_init: str):
    photo_kb = InlineKeyboardBuilder()
    match kb_init:
        case 'start':
            photo_kb.add(types.InlineKeyboardButton(text='Следующая',
                                                    callback_data='photo_next'))
        case 'mid':
            photo_kb.add(types.InlineKeyboardButton(text='Предыдущая',
                                                    callback_data='photo_prev'))
            photo_kb.add(types.InlineKeyboardButton(text='Следующая',
                                                    callback_data='photo_next'))
        case 'end':
            photo_kb.add(types.InlineKeyboardButton(text='Предыдущая',
                                                    callback_data='photo_prev'))

    photo_kb.row(types.InlineKeyboardButton(text='Назад',
                                            callback_data='to_items'))
    return photo_kb


def create_close_kb():
    close_kb = InlineKeyboardBuilder()
    close_kb.button(text='В главное меню',
                    callback_data=CloseCallback(action='close').pack())
    return close_kb