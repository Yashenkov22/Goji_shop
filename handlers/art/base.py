from typing import Union

from aiogram import types, Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)

from utils.keyboards.art_keyboards import create_all_artists_kb

art_router = Router()

@art_router.message(F.text == 'Музыка')
async def music_section(message: types.Message,
                        state: FSMContext,
                        session: AsyncSession,
                        bot: Bot):
    await try_delete_prev_message(bot, state)

    all_artists_kb = await create_all_artists_kb(session)

    await message.answer('Выбери иполнителя',
                         disable_notification=True,
                         reply_markup=all_artists_kb.as_markup())
    
    await message.delete()

