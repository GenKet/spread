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

def kick(time_out, user_id):
    time.sleep(time_out)
    Database.upd_status(0, -1, user_id)


async def check(token):
    basic = HTTPBasicAuth('25332', '79588228d9f50034fc476444807a8cb9d58b34f02504467aa18d5e001e4e9db4')
    r = requests.get(f"https://checkout.bepaid.by/ctp/api/checkouts/{token}", auth=basic)
    print(r.text)
    r = r.json()
    status = r["checkout"]["status"]
    if status == "successful":
        return True
    else:
        return False



async def payments(product_id):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-Version": "2",
    }

    basic = HTTPBasicAuth('25332', '79588228d9f50034fc476444807a8cb9d58b34f02504467aa18d5e001e4e9db4')

    r = requests.get(f'https://api.bepaid.by/products/{product_id}', auth=basic)
    r = r.json()
    description = r["description"]
    amount = r["amount"]
    amount1 = float(amount / 100)
    currency = r["currency"]
    pay_url = r["pay_url"]
    payment_url = r["payment_url"]
    confirm_url = r["confirm_url"]

    data = {
        "checkout": {
            "transaction_type": "payment",
            "attempts": 3,
            "settings": {

                "return_url": "http://127.0.0.1:4567/return",
                "success_url": "http://127.0.0.1:4567/success",
                "decline_url": "http://127.0.0.1:4567/decline",
                "fail_url": "http://127.0.0.1:4567/fail",
                "cancel_url": "http://127.0.0.1:4567/cancel",
                "notification_url": "http://your_shop.com/notification",
                "button_text": f"Оплатить {amount1} {currency}",
                "button_next_text": "Вернуться в магазин",
                "language": "ru",
                "customer_fields": {
                    "visible": ["first_name", "last_name", "country", "phone", "birth_date", "email"],
                },
            },
            "payment_method": {
                "types": ["credit_card"]
            },
            "order": {
                "currency": currency,
                "amount": amount,
                "description": description
            },
            "customer": {
            }
        }
    }

    r = requests.post('https://checkout.bepaid.by/ctp/api/checkouts', json=data, auth=basic, headers=headers)
    r = r.json()
    token = r["checkout"]["token"]
    url = r["checkout"]["redirect_url"]

    r = requests.get(f"https://checkout.bepaid.by/ctp/api/checkouts/{token}", auth=basic)
    print(r.text)
    r = r.json()

    status = r["checkout"]["status"]
    stat_tok = [token, status, url]
    return stat_tok




def free_spread(text_1, text_2, text_3, current_chat):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if current_time == "08:00:00":
        bot.send_message(current_chat,text_1)
        time.sleep(86400)
        bot.send_message(current_chat, text_2)
        time.sleep(86400)
        bot.send_message(current_chat,text_3)
        bot.send_message(current_chat,"Сегодня заканчивается бесплатный доступ к моим информационным ресурсам! И я буду рада быть тебе полезной и в дальнейшем!\nПриглашаю тебя продолжить наше знакомство, для этого тебе нужно выбрать любой тариф!",reply_markup=upst_markup)


@dp.message_handler(state=spread.name_us)
async def get_name(message: types.Message, state:FSMContext ):
    async with state.proxy() as data_storage:
        name = message.text
        data_storage["user_id"] = message.from_user.id
        data_storage["name"] = name
        await bot.send_message(message.chat.id,
            f"Рада нашему знакомству,{name}\n\nТеперь я буду всегда с тобой, как матрица, в которой мы все находимся\n\nНапиши, пожалуйста, ниже, из какого ты города.", reply_markup=back_markup)
        await spread.city.set()


@dp.message_handler(state=spread.city)
async def get_city(message: types.Message, state:FSMContext ):
    if message.text == "Назад":
        await message.reply(
            "Приветствую тебя, дорогой!\n\nМеня зовут Тринити! Я нумерологический бот-помощник и твой проводник в мир цифр.\n\nА как зовут тебя?\n\nВведи, пожалуйста, своё имя ниже", reply_markup=back_markup)
        await spread.name_us.set()
    else:
        async with state.proxy() as data_storage:
            city = message.text
            data_storage["city"] = city
            await bot.send_message(message.chat.id,
                f"Могу с уверенностью сказать, что ты сейчас находишься именно в том месте, в котором ты должен находиться!Но ты всегда можешь всё изменить, если захочешь! А твои цифры подскажут как!\n\nДаже цифры в твоём номере телефона имеют значение!\n\nКстати, напиши, пожалуйста, ниже свой номер телефона.", reply_markup=back_markup)
            await spread.ph_number.set()


@dp.message_handler(state=spread.ph_number)
async def get_ph(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with state.proxy() as data_storage:
            name = data_storage["name"]
            await bot.send_message(message.chat.id,
                                   f"Рад нашему знакомству,{name}\n\nТеперь я буду всегда с тобой, как матрица, в которой мы все находимся\n\nНапиши, пожалуйста, ниже, из какого ты города.",
                                   reply_markup=back_markup)
            await spread.city.set()
    else:
        async with state.proxy() as data_storage:
            phone = message.text
            data_storage["ph_number"] = phone
            await bot.send_message(message.chat.id,
                                   f"Спасибо! Теперь будем на связи!\n\nЧтобы рассчитать твой прогноз, мне нужна твоя дата рождения!\n\nВведи её, пожалуйста, ниже в формате дд.мм.гггг\n\nНапример: 10.08.2023", reply_markup=back_markup)
            await spread.bithday.set()


@dp.message_handler(state=spread.bithday)
async def get_bithday(message: types.Message, state:FSMContext ):
    if message.text == "Назад":
        await bot.send_message(message.chat.id,
                               f"Могу с уверенностью сказать, что ты сейчас находишься именно в том месте, в котором ты должен находиться!Но ты всегда можешь всё изменить, если захочешь! А твои цифры подскажут как!\n\nДаже цифры в твоём номере телефона имеют значение!\n\nКстати, напиши, пожалуйста, ниже свой номер телефона.", reply_markup=back_markup)
        await spread.ph_number.set()
    else:
        async with state.proxy() as data_storage:
            bithday = message.text
            data_storage["bithday"] = bithday
            await bot.send_message(message.chat.id,
                f"Проверь данные, всё верно?\n{bithday}",reply_markup=start_in)


@dp.callback_query_handler(Text(equals='yes'), state=spread.bithday)
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        name = data_storage["name"]
        city = data_storage["city"]
        ph_number = data_storage["ph_number"]
        bithday = data_storage["bithday"]
        user_id = data_storage["user_id"]
        Database.add_info(name,city,ph_number,bithday,user_id)
        message_text = f'В честь нашего знакомства я ДАРЮ тебе доступ к моим возможностям на ТРИ дня!\n\nНикуда не уходи, я почти закончила  расчёт твоего прогноза на сегодня'
        await bot.send_message(callback_query.message.chat.id,text=message_text, reply_markup=get_prognoz_markup)
        await spread.accept.set()


@dp.callback_query_handler(Text(equals='again'), state=spread.bithday)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        message_text = f'Введи, пожалуйста, дату рождения в формате дд.мм.гггг'
        await callback_query.message.edit_text(text=message_text)
        await spread.bithday.set()


@dp.message_handler(state=spread.accept)
async def get_prognoz(message: types.Message, state:FSMContext):
    async with state.proxy() as data_storage:
        now = datetime.now()
        current_day = now.day
        current_month = now.month
        current_time = now.strftime("%H:%M:%S")
        bithday = data_storage["bithday"]
        value_1 = random.randint(0,9)
        value_2 = int(value_1) + 1
        if value_2 > 9:
            value_2 = 1
        value_3 = value_2 + 1
        if value_3 > 9:
            value_3 = 1

        text_1 = translate.get(value_1)
        text_2 = translate.get(value_2)
        text_3 = translate.get(value_3)
        current_chat = message.chat.id
        text_1 = "Доброе утро!\nГотов твой прогноз на сегодня:\n" + text_1
        t1 = threading.Thread(target=free_spread, args=(text_1,text_2,text_3,current_chat))
        t1.start()
        await bot.send_message(message.chat.id, "А давай я ещё тебе расскажу подробнее о том, как ты сможешь получать свой прогноз.\n\nПакет'ПРЕМИУМ'\nДействует в течении года.\nВключает в сеья прогноз на каждый день, на месяц и на текущий год.\nСтоимость - 140$\n\nПакет'ВЫХОД ИЗ МАТРИЦЫ'\nДействует в течении месяца.\nВключает в себя прогноз на каждый день, на текущий месяц и на текущий год.\nСтоимость - 14$\n\nПакет'ПЕРЕХОД'\nДействует в течении месяца.\nВключает в себя 15 запросов на прогноза на день и прогноз на текущий месяц.\nСтоимость - 12$\n\nПакет'НАЧАЛО'\nДействует в течении месяца.\nВключает в себя 8 запросов прогноза на день\nСтоимость - 8$", reply_markup=upst_markup)
        await bot.send_message(message.chat.id, "Удачного тебе дня!\nУшла делать расчет твоего прогноза на следующий день!\nВстретимся завтра утром!")
        await spread.upst.set()
    # except:
    #     pass


@dp.message_handler(state=spread.upst)
async def upst(message: types.Message, state:FSMContext):
    async with state.proxy() as data_storage:
        if message.text == "Начало":
            product_id = "prd_2c7478647cf6bd3d"
            result = await payments(product_id)
            await bot.send_message(message.chat.id,f"Для оплаты перейдите по ссылке:{result[2]}", reply_markup=check_markup)
            token = result[0]
            data_storage["count"] = 8
            data_storage["token"] = token
            data_storage["status"] = 1
        elif message.text == "Переход":
            product_id = "prd_6a124cdf81291202"
            result = await payments(product_id)
            await bot.send_message(message.chat.id,f"Для оплаты перейдите по ссылке:{result[2]}", reply_markup=check_markup)
            token = result[0]
            data_storage["count"] = 15
            data_storage["token"] = token
            data_storage["status"] = 2
        elif message.text == "Выход из матрицы":
            product_id = "prd_d9ba5236d4a48596"
            result = await payments(product_id)
            await bot.send_message(message.chat.id,f"Для оплаты перейдите по ссылке:{result[2]}", reply_markup=check_markup)
            token = result[0]
            data_storage["count"] = 0
            data_storage["token"] = token
            data_storage["status"] = 3
        elif message.text == "Премиум":
            product_id = "prd_6b93b3a3b8870a01"
            result = await payments(product_id)
            await bot.send_message(message.chat.id,f"Для оплаты перейдите по ссылке:{result[2]}", reply_markup=check_markup)
            token = result[0]
            data_storage["count"] = 0
            data_storage["token"] = token
            data_storage["status"] = 4
        elif message.text == "Назад":
            await state.finish()


@dp.callback_query_handler(Text(equals='check'), state=spread.upst)
async def next_result(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data_storage:
        token = data_storage["token"]
        result = await check(token)
        if result == True:
            count = data_storage["count"]
            status = data_storage["status"]
            await bot.send_message(callback_query.message.chat.id, "Успешно оплачено!",reply_markup=get_markup)
            await Database.upd_status(status, count,callback_query.message.from_user.id)
            await state.finish()
            if status == 3:
                time_out = 2592000
                t2 = threading.Thread(target=kick, args=(time_out,callback_query.message.from_user.id))
                t2.start()
            elif status == 4:
                time_out = 31104000
                t2 = threading.Thread(target=kick, args=(time_out,callback_query.message.from_user.id))
                t2.start()
        else:
            await bot.send_message(callback_query.message.chat.id,"Ожидаю подтверждение платежа, проверьте платеж позже")
            await spread.upst.set()


