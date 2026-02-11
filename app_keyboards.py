from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


keyboard = [[KeyboardButton(text='Описание бота'),
             KeyboardButton(text='Команды')]]
kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True,
                         input_field_placeholder="Выберите пункт меню...")

# Сделать клавиатуру в линию, а не столбик
def make_categories_kb(category_list):
    kb_categories = []
    for category in category_list:
        kb_categories.append([KeyboardButton(text=category)])

    keyboard_categories = ReplyKeyboardMarkup(keyboard=kb_categories,
                                          resize_keyboard=True)
    return keyboard_categories
