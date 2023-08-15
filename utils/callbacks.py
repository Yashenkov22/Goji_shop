from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix='cat'):
    category: str


class ConfirmCallback(CallbackData, prefix='confirm'):
    confirm: str


class CloseCallback(CallbackData, prefix='close'):
    action: str


class AddCategoryCallback(CallbackData, prefix='add_cat'):
    category: str
