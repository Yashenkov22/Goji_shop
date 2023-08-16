from typing import Optional

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbacks import ConfirmCallback


def kb_with_cancel_btn(keyboard: Optional[InlineKeyboardBuilder] = None):
    if keyboard is None:
        keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text='Отмена действия',
                                              callback_data=ConfirmCallback(confirm='no').pack()))
    return keyboard