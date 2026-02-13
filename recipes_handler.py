# Файл recipes_handler.py должен содержать обработчики для взаимодействия
# с API themealdb.

import aiohttp
from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup

from random import choices
from googletrans import Translator

from app_keyboards import make_categories_kb, show_recipe_kb

class SearchRecipe(StatesGroup):
    waiting_for_category = State()
    random_recipe = State()
    waiting_for_recipe = State()


router = Router()
translator = Translator()

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
            categories_list = data.get('meals', [])
            categories = [category['strCategory']
                          for category in categories_list]
            return categories


@router.message(SearchRecipe.waiting_for_category)
async def meals_by_category(message: Message, state: FSMContext):
    """
    Selects random recipes. Number of random recipes = what the user entered
    after the command /category_search_random
    """
    user_recipe_count = await state.get_data()
    recipe_count = user_recipe_count.get('recipe_count', 1)

    category = message.text
    url = (f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meals_list = data.get('meals', [])

    if not meals_list:
        await message.answer('Recipe not found!')
        return

    random_meals = choices(meals_list, k=recipe_count)
    random_meals_id = [meal['idMeal'] for meal in random_meals]
    await state.update_data(random_meals_id=random_meals_id)

    response = 'Your recipes are: \n'
    for meal in random_meals:
        en_name = meal.get('strMeal')
        translation = translator.translate(en_name, dest='ru')
        response += f'{translation.text}\n'

    keyboard = show_recipe_kb()
    await state.set_state(SearchRecipe.waiting_for_recipe)
    await message.answer(response, reply_markup=keyboard)
