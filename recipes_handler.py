import aiohttp
import asyncio
from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Bold, as_marked_list, as_list
from aiogram import html

from random import choices
from googletrans import Translator

from app_keyboards import make_categories_kb, show_recipe_kb

class SearchRecipe(StatesGroup):
    waiting_for_category = State()
    waiting_for_recipe = State()


router = Router()
translator = Translator()

@router.message(Command('category_search_random'))
async def category_search_random(message: Message, command: CommandObject,
                                state: FSMContext):
    if command.args and command.args.isdigit():
        count = int(command.args)
    else:
        await message.answer('Пожалуйста, введите число! Например: '
                             '/category_search_random 3')
        return

    await state.update_data(recipe_count=count)
    category_list = await get_categories()

    categories = []
    for category in category_list:
        translation = translator.translate(category, dest='ru').text
        categories.append(f'{category} — {translation.lower()}')

    hint_message = as_list(
        Bold('Пожалуйста, выберите категорию: \n'),
        as_marked_list(
            *categories,
            marker='· '
        )
    )

    keyboard = make_categories_kb(category_list)
    await state.set_state(SearchRecipe.waiting_for_category)
    await message.answer(hint_message.as_html(), reply_markup=keyboard)


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
    url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            meals_list = data.get('meals', [])

    if not meals_list:
        await message.answer('Рецепты не найдены!')
        return

    if len(meals_list) < recipe_count:
        await message.answer(f"В этой категории только {len(meals_list)} рецептов. "
                             f"Вот все рецепты из этой категории:")

    min_recipe_count = min(recipe_count, len(meals_list))
    random_meals = choices(meals_list, k=min_recipe_count)
    random_meals_id = [meal['idMeal'] for meal in random_meals]
    await state.update_data(random_meals_id=random_meals_id)
    await state.update_data(random_meals_name=random_meals)

    response = html.bold('Ваши рецепты:') + '\n'
    for meal in random_meals:
        en_name = meal.get('strMeal')
        translation = translator.translate(en_name, dest='ru').text
        response += f'·  {translation}\n'

    keyboard = show_recipe_kb()
    await state.set_state(SearchRecipe.waiting_for_recipe)
    await message.answer(response, reply_markup=keyboard, parse_mode='HTML')


@router.message(SearchRecipe.waiting_for_recipe)
async def get_random_recipe(message: Message, state: FSMContext):
    """
    Send random recipes to the user.
    """
    user_data = await state.get_data()
    meals_id = user_data.get('random_meals_id', [])

    if not meals_id:
        await message.answer('Список рецептов пуст!')
        return

    await message.answer("Готовлю инструкции, это может занять минуту... ")

    async with aiohttp.ClientSession() as session:
        for meal_id in meals_id:
            url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'
            async with session.get(url) as resp:
                data = await resp.json()
                meal_data = data.get('meals')[0] if data.get('meals') else None

                if meal_data:
                    en_meal = meal_data.get('strMeal')
                    en_instr = meal_data.get('strInstructions')

                    ru_meal = translator.translate(en_meal, dest='ru').text
                    ru_instr = translator.translate(en_instr, dest='ru').text

                    meal_bold = html.bold(ru_meal)
                    instr = html.quote(ru_instr)
                    recipe_message = f'{meal_bold}: \n\n {instr}\n\n'

                    if len(recipe_message) > 4096:
                        recipe_message = recipe_message[:4096]

                    await message.answer(recipe_message, parse_mode='HTML')

    await state.clear()

