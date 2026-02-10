import asyncio

from aiogram import Dispatcher, Bot
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_marked_list, as_list, as_line

from token_data import TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """ Start command handler """
    content = as_list(
        as_line('Hello ', Bold(message.from_user.full_name), "!"),
        "This bot will tell you the recipes and what ingredients are needed "
        "for each recipe.",
        "\n",
        as_marked_list(
            Bold("Commands:"),
            '/description',
            marker='⯏'
        )
    )
    await message.answer(content.as_html())


@dp.message(Command('description'))
@dp.message(F.text.casefold() == 'описание бота')
async def command_description_handler(message: Message):
    """ Bot Description command handler """
    content = 'This bot provides information about recipies & ingredients!'
    await message.answer(content)



@dp.message(Command('commands'))
@dp.message(F.text.casefold() == 'команды')
async def commands_handler(message: Message):
    """The list of available commands"""
    content = as_list(
        Bold("Команды: "),
        as_marked_list('/start',
        '/description',
        '/commands',
        marker='⯏'
        )
    )
    await message.answer(content.as_html())


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Closing bot!')
