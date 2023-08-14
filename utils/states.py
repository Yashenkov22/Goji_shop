from aiogram.fsm.state import State, StatesGroup


class AdminCategory(StatesGroup):
    name = State()


class AdminItem(StatesGroup):
    category = State()
    name = State()
    price = State()