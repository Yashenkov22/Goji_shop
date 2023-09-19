from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import select_all_artists


def create_art_kb():
    art_kb = ReplyKeyboardBuilder()
    art_kb.add(types.KeyboardButton(text='Музыка'))
    art_kb.add(types.KeyboardButton(text='Клипы'))
    art_kb.row(types.KeyboardButton(text='В главное меню'))
    
    return art_kb


async def create_all_artists_kb(session: AsyncSession,
                                prefix: str = 'artist'):
    all_artists = await select_all_artists(session)

    all_artists_kb = InlineKeyboardBuilder()

    for artist in all_artists:
        all_artists_kb.row(types.InlineKeyboardButton(text=artist[0],
                                                      callback_data=f'{prefix}_{artist[0]}'))
    
    if prefix == 'artist':
        all_artists_kb.row(types.InlineKeyboardButton(text='Назад',
                                                    callback_data=f'to_art'))
    
    return all_artists_kb