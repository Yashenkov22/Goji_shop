from typing import Any

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext


async def try_delete_prev_message(bot: Bot,
                                  state: FSMContext):
    data = await state.get_data()

    if data.get('prev_msg') and data['prev_msg']:
        prev_msg = data['prev_msg']

        for msg in prev_msg:
            await bot.delete_message(*msg)

        await state.update_data(prev_msg=None)
    else:
        pass


def add_message_for_delete(data: dict[str, Any],
                           msg: types.Message):
    data['prev_msg'].append((msg.chat.id, msg.message_id))