from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqlalchemy.orm import Session

from utils.callbacks import ConfirmCallback, AddCategoryCallback
from db.queries import get_all_categories


#Admin keyboard
def create_admin_kb():
    admin_kb = ReplyKeyboardBuilder()
    admin_kb.row(types.KeyboardButton(text='Добавить категорию'))
    admin_kb.row(types.KeyboardButton(text='Добавить товар'))
    admin_kb.row(types.KeyboardButton(text='Изменить товар'))
    admin_kb.row(types.KeyboardButton(text='Удалить товар'))
    admin_kb.row(types.KeyboardButton(text='На главную'))
    
    return admin_kb


def create_confirm_kb():
    confirm_kb = InlineKeyboardBuilder()
    confirm_kb.add(types.InlineKeyboardButton(text='ДА',
                                              callback_data=ConfirmCallback(confirm='yes').pack()))
    confirm_kb.add(types.InlineKeyboardButton(text='НЕТ',
                                              callback_data=ConfirmCallback(confirm='no').pack()))
    
    return confirm_kb


def category_list_for_add(session: Session):
    category_list = get_all_categories(session)
    
    category_kb = InlineKeyboardBuilder()
    for cat in category_list:
        category_kb.button(text=cat[0],
                           callback_data=AddCategoryCallback(category=cat[0]))
    return category_kb