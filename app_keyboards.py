from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


keyboard = [[KeyboardButton(text='Описание бота'),
             KeyboardButton(text='Команды')]]
kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True,
                         input_field_placeholder="Выберите пункт меню...")


def make_categories_kb(category_list):
    builder = ReplyKeyboardBuilder()

    for category in category_list:
        builder.add(KeyboardButton(text=category))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def show_recipe_kb():
    kb = [[KeyboardButton(text='Покажи рецепты')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard