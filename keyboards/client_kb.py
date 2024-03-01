from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

ikb_client_start = InlineKeyboardMarkup(row_width=1)#, one_time_keyboard=True)

b1 = InlineKeyboardButton(text='🏥 Запрос на госпитализацию', callback_data="main_page")

ikb_client_start.add(b1)

ikb_client_main = InlineKeyboardMarkup(row_width=1)#, one_time_keyboard=True)

b2_1 = InlineKeyboardButton(text='🧭 Главное меню', callback_data="start_page")

ikb_client_main.add(b2_1)
#b2 = InlineKeyboardButton(text='🧠 Алгоритмы МОССМП')
#b3 = KeyboardButton('Поделиться номером', request_contact=True)
#b4 = KeyboardButton('Отправить где я', request_location=True)

