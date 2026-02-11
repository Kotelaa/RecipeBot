# Файл recipes_handler.py должен содержать обработчики для взаимодействия
# с API themealdb.

import aiohttp
from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup

from random import choice

from app_keyboards import make_categories_kb

class SearchRecipe(StatesGroup):
    waiting_for_category = State()
    waiting_for_recipe = State()


router = Router()

@router.message(Command('category_search_random'))
async def category_search_random(message: Message, command: CommandObject,
                                state: FSMContext):
    if command.args and command.args.isdigit():
        count = int(command.args)
    else:
        await message.answer('Please enter a number! For example: '
                             '/category_search_random 3')
        return

    await state.update_data(recipe_count=count)
    category_list = await get_categories()
    keyboard = make_categories_kb(category_list)
    await state.set_state(SearchRecipe.waiting_for_category)
    await message.answer('Please, select a category!',
                         reply_markup=keyboard)


async def get_categories():
    url = f'https://www.themealdb.com/api/json/v1/1/list.php?c=list'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            categories_list = data.get('meals')
            categories = [category['strCategory']
                          for category in categories_list]
            return categories


