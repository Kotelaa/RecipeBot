from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


keyboard = [[KeyboardButton(text='Описание бота'),
             KeyboardButton(text='Команды')]]
kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True,
                         input_field_placeholder="Выберите пункт меню...")


def make_categories_kb(category_list):
    row = []
    kb_categories = []

    for category in category_list:
        row.append(KeyboardButton(text=category))
        if len(row) == 3:
            kb_categories.append(row)
            row = []

    if row:
        kb_categories.append(row)

    keyboard_categories = ReplyKeyboardMarkup(keyboard=kb_categories,
                                          resize_keyboard=True)
    return keyboard_categories


def show_recipe_kb():
    kb = [[KeyboardButton(text='Покажи рецепты')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard