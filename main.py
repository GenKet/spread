from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State,StatesGroup

from config import TOKEN
from db import BotDB

Database = BotDB("spread.db")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

from handler import *

class spread(StatesGroup):
    name_us = State()
    city = State()
    ph_number = State()
    bithday = State()
    accept = State()
    upst = State()


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    if not(Database.user_exists(message.from_user.id)):
        Database.add_user(message.from_user.id)
    await message.reply("Приветствую тебя, дорогой!\n\nМеня зовут Тринити! Я нумерологический бот-помощник и твой проводник в мир цифр.\n\nА как зовут тебя?\n\nВведи, пожалуйста, своё имя ниже")
    await spread.name_us.set()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)