from aiogram import types

back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
back = types.KeyboardButton("Назад")
cancel = types.KeyboardButton("Отмена")
back_markup.add(back,cancel)

get_prognoz_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_prognoz = types.KeyboardButton("Получить прогноз")
get_prognoz_markup.add(get_prognoz)

upst_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start = types.KeyboardButton("Начало")
prem = types.KeyboardButton("Премиум")
matrix = types.KeyboardButton("Выход из матрицы")
perech = types.KeyboardButton("Переход")
upst_markup.add(start, perech, matrix, prem)
upst_markup.row(back)