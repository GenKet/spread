from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_in = InlineKeyboardMarkup(row_width=1)
yes = InlineKeyboardButton('Да', callback_data='yes')
again = InlineKeyboardButton('Ввести заново', callback_data='again')
start_in.add(yes, again)

check_markup = InlineKeyboardMarkup(row_width=1)
check = InlineKeyboardButton("Проверить оплату", callback_data="check")
check_markup.add(check)