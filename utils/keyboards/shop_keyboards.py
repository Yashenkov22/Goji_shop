from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqlalchemy.orm.session import Session

from utils.callbacks import CloseCallback
from db.queries import get_all_categories, get_items_for_current_category
from config import ADMIN_IDS


#Keyboard on main page
def create_main_kb(user_id):

    main_kb = ReplyKeyboardBuilder()
    main_kb.row(types.KeyboardButton(text='Ассортимент'))
    main_kb.row(types.KeyboardButton(text='Промо'))
    main_kb.row(types.KeyboardButton(text='Подробности'))
    if user_id in ADMIN_IDS:
        main_kb.row(types.KeyboardButton(text='Админ панель'))
    return main_kb

#Inline keyboard categories
def create_category_kb(session: Session, prefix: str = 'cat') -> InlineKeyboardBuilder:
    category_list = get_all_categories(session)
    category_kb = InlineKeyboardBuilder()
    for cat in category_list:
        category_kb.row(
            types.InlineKeyboardButton(text=cat[0],
                                       callback_data=f'{prefix}:{cat[0]}')
        )
    category_kb.row(types.InlineKeyboardButton(text='Назад',
                                               callback_data='to_main'))
    return category_kb


#Inline keyboard items
def create_items_kb(category: str,
                    session: Session,
                    prefix: str = 'show_item') -> InlineKeyboardBuilder:
    item_list = get_items_for_current_category(category, session)

    item_kb = InlineKeyboardBuilder()
    for item in item_list:
        item_kb.row(types.InlineKeyboardButton(text=item[1],
                                               callback_data=f'{prefix}:{item[1]}'))
    if prefix == 'show_item':
        item_kb.row(types.InlineKeyboardButton(text='Назад',
                                            callback_data='to_categories'))
    return item_kb



def create_close_kb():
    close_kb = InlineKeyboardBuilder()
    close_kb.button(text='Закрыть',
                    callback_data=CloseCallback(action='close').pack())
    return close_kb