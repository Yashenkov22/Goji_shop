from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    name = State()


class AddItem(StatesGroup):
    category = State()
    name = State()
    price = State()


class DeleteItem(StatesGroup):
    category = State()
    name = State()


class EditItem(StatesGroup):
    old_item = State()
    name = State()
    price = State()


class AddPhoto(StatesGroup):
    pass