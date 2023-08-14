from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks import CloseCallback


close_kb = InlineKeyboardBuilder()
close_kb.button(text='Закрыть',
                callback_data=CloseCallback(action='close').pack())