from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.callbacks import ConfirmCallback


#Admin keyboard
def create_admin_kb():
    admin_kb = ReplyKeyboardBuilder()
    admin_kb.row(types.KeyboardButton(text='Добавить категорию'))
    admin_kb.row(types.KeyboardButton(text='Добавить товар'))
    admin_kb.row(types.KeyboardButton(text='Изменить товар'))
    admin_kb.row(types.KeyboardButton(text='Добавить фото к товару'))
    admin_kb.row(types.KeyboardButton(text='Удалить товар'))
    admin_kb.row(types.KeyboardButton(text='На главную'))
    
    return admin_kb


#Confirm Inline keyboard
def create_confirm_kb():
    confirm_kb = InlineKeyboardBuilder()
    confirm_kb.add(types.InlineKeyboardButton(text='ДА',
                                              callback_data=ConfirmCallback(confirm='yes').pack()))
    confirm_kb.add(types.InlineKeyboardButton(text='НЕТ',
                                              callback_data=ConfirmCallback(confirm='no').pack()))
    
    return confirm_kb


def load_photo_kb():
    photo_kb = ReplyKeyboardBuilder()
    photo_kb.row(types.KeyboardButton(text='Продолжить'))
    return photo_kb