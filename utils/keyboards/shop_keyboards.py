from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqlalchemy.orm.session import Session
from sqlalchemy import select

from db.models import categories, items
from db.queries import get_all_categories
from ..callbacks import CategoryCallback
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
def create_category_kb(session: Session) -> InlineKeyboardBuilder:
    category_list = get_all_categories(session)
    category_kb = InlineKeyboardBuilder()
    for cat in category_list:
        category_kb.row(
            types.InlineKeyboardButton(text=cat[0],
                                       callback_data=CategoryCallback(category=cat[0]).pack())
        )
    category_kb.row(types.InlineKeyboardButton(text='Назад',
                                               callback_data='to_main'))
    return category_kb


#Inline keyboard items
def create_items_kb(category: str, session: Session) -> InlineKeyboardBuilder:
    item_list = session.execute(select(items).where(items.c.category == category)).all()

    item_kb = InlineKeyboardBuilder()
    for item in item_list:
        item_kb.row(types.InlineKeyboardButton(text=item[1],
                                               callback_data='qqqq'))
    item_kb.row(types.InlineKeyboardButton(text='Назад',
                                           callback_data='to_categories'))
    return item_kb


