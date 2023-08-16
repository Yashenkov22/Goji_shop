from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from utils.states import AddCategory
from utils.keyboards.admin_keyboards import create_confirm_kb

category_router = Router()

@category_router.message(F.text == 'Добавить категорию')
async def create_category(message: types.Message, state: FSMContext):
    await state.update_data(action='add_cat')
    await state.set_state(AddCategory.name)
    await message.answer('Напиши название новой категории\n<b>Максимальная длина 21 символ</b>', parse_mode='html')


@category_router.message(AddCategory.name)
async def start_category(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(f'Создать категорию <b>{message.text.capitalize()}</b>?',
                         reply_markup=create_confirm_kb().as_markup(),
                         parse_mode='html')