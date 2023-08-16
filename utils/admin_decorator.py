from aiogram import types
from config import ADMIN_IDS

def admin_only(func):
    async def wrapped(*args, **kwargs):
        message = None
        for arg in args:
            if isinstance(arg, (types.Message, types.CallbackQuery)):
                message = arg
                break
        if message.from_user.id in ADMIN_IDS:
            return await func(*args, **kwargs)
        else:
            return await message.answer('Доступ запрещен!')
    return wrapped