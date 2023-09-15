from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import ADMIN_IDS
from utils.callbacks import CloseCallback


def create_main_kb(user_id: int):
    main_kb = ReplyKeyboardBuilder()
    main_kb.add(types.KeyboardButton(text='Товары'))
    main_kb.add(types.KeyboardButton(text='Творчество'))

    if user_id in ADMIN_IDS:
        main_kb.row(types.KeyboardButton(text='Админ панель'))

    return main_kb


# def create_close_kb():
#     close_kb = InlineKeyboardBuilder()
#     close_kb.button(text='В главное меню',
#                     callback_data=CloseCallback(action='close').pack())
#     return close_kb

def create_close_kb(what: str):
    close_kb = InlineKeyboardBuilder()
    
    txt = 'В главное меню' if what =='promo' else 'Назад в раздел'
    close_kb.button(text=txt,
                    callback_data=CloseCallback(action=f'close_{what}').pack())
    return close_kb