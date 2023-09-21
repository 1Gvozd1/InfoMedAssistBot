from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('🏥 Запрос на госпитализацию')
b2 = KeyboardButton('🧠 Алгоритмы МОССМП')
#b3 = KeyboardButton('Поделиться номером', request_contact=True)
#b4 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup()#, one_time_keyboard=True)


kb_client.add(b1).add(b2)