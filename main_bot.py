import asyncio

from aiogram import Dispatcher, Bot, Router
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_marked_list, as_list, as_line

from token_data import TOKEN
from app_keyboards import kb
from recipes_handler import router as router_recipe

dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    """ Start command handler """
    content = as_list(
        as_line('Привет, ', Bold(message.from_user.full_name), "!"),
        "Этот бот поможет вам найти рецепты и подскажет, какие ингредиенты "
        "нужны для каждого блюда 🍵 \n",
        Bold("Доступные команды:"),
        as_marked_list(
            '/description — описание бота',
            '/commands — список всех команд',
            '/category_search_random — поиск по категориям',
            marker='· '
        )
    )
    await message.answer(content.as_html(), reply_markup=kb)


@router.message(Command('description'))
@router.message(F.text.casefold() == 'описание бота')
async def command_description_handler(message: Message):
    """ Bot Description command handler """
    content = ('Этот бот предоставляет подробную информацию о рецептах '
               'и необходимых ингредиентах! 🍵')
    await message.answer(content)


@router.message(Command('commands'))
@router.message(F.text.casefold() == 'команды')
async def commands_handler(message: Message):
    """The list of available commands"""
    content = as_list(
        Bold("Команды: "),
        as_marked_list('/start',
        '/description',
        '/category_search_random',
        marker='· '
        )
    )
    await message.answer(content.as_html())


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router_recipe)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
