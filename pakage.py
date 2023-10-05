import time
import random
from main import dp, bot, spread
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import json
import xlwings as xw
import pandas

import openpyxl
import threading

from markup import back_markup, get_prognoz_markup, upst_markup, get_markup
from inline_markup import start_in, check_markup
from main import Database
from dict import translate,month,days


def get_prognoz():
    value_1 = random.randint(0, 9)
    return value_1



@dp.message_handler(Text(equals="Приступим к моему пакету"))
async def get_name(message: types.Message, state:FSMContext ):
    async with state.proxy() as data_storage:
        result = Database.get_status(message.from_user,id)
        if result == 1:
            pass
        elif result == 2:
            pass
        elif result == 3:
            pass
        elif result == 4:
            pass