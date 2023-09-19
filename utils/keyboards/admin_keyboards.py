from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.callbacks import ConfirmCallback


#Admin keyboard
def create_admin_kb():
    admin_kb = ReplyKeyboardBuilder()
    admin_kb.row(types.KeyboardButton(text='Управление категориями'))
    admin_kb.row(types.KeyboardButton(text='Управление товарами'))
    admin_kb.row(types.KeyboardButton(text='Управление фото'))
    admin_kb.row(types.KeyboardButton(text='Управление артистами'))

    admin_kb.row(types.KeyboardButton(text='На главную'))
    
    return admin_kb


def create_manage_category_kb():
    manage_cat_kb = ReplyKeyboardBuilder()
    manage_cat_kb.row(types.KeyboardButton(text='Добавить категорию'))
    manage_cat_kb.row(types.KeyboardButton(text='Удалить категорию'))

    return manage_cat_kb


def create_manage_item_kb():
    manage_item_kb = ReplyKeyboardBuilder()
    manage_item_kb.row(types.KeyboardButton(text='Добавить товар'))
    manage_item_kb.row(types.KeyboardButton(text='Изменить товар'))
    manage_item_kb.row(types.KeyboardButton(text='Удалить товар'))

    return manage_item_kb


def create_manage_photo_kb():
    manage_photo_kb = ReplyKeyboardBuilder()
    manage_photo_kb.row(types.KeyboardButton(text='Добавить фото к товару'))
    manage_photo_kb.row(types.KeyboardButton(text='Удалить фото в товаре'))


    return manage_photo_kb

def create_to_abmin_page_kb(keyboard: ReplyKeyboardBuilder):
    keyboard.row(types.KeyboardButton(text='Назад в админ панель'))

    return keyboard


def create_manage_artist_kb():
    manage_artist_kb = ReplyKeyboardBuilder()
    manage_artist_kb.row(types.KeyboardButton(text='Добавить артиста'))
    manage_artist_kb.row(types.KeyboardButton(text='Удалить артиста'))

    return manage_artist_kb


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


#Inline photo delete keyboard
def create_photo_delete_keyboard(kb_init: str):
    photo_kb = InlineKeyboardBuilder()

    match kb_init:
        case 'start':
            photo_kb.add(types.InlineKeyboardButton(text='Следующая',
                                                    callback_data='del_photo_next'))
        case 'mid':
            photo_kb.add(types.InlineKeyboardButton(text='Предыдущая',
                                                    callback_data='del_photo_prev'))
            photo_kb.add(types.InlineKeyboardButton(text='Следующая',
                                                    callback_data='del_photo_next'))
        case 'end':
            photo_kb.add(types.InlineKeyboardButton(text='Предыдущая',
                                                    callback_data='del_photo_prev'))
            
    photo_kb.row(types.InlineKeyboardButton(text='Удалить фото',
                                            callback_data='photo_delete'))
    
    photo_kb.row(types.InlineKeyboardButton(text='Отмена действия',
                                            callback_data='to_admin_page'))
    return photo_kb