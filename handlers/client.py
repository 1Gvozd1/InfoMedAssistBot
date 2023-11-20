import asyncio

from aiogram import Dispatcher

from Whisper import WhisperRecognizer
from stt import AsyncSTT
from create_bot import bot
from keyboards import ikb_client_main, ikb_client_start
from aiogram.types import InputMedia
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import os
from pathlib import Path
import concurrent.futures
from data_base import sqlite_db


dp= Dispatcher(bot)

# whisper = WhisperRecognizer()
from transcriber import Transcriber

transcriber = Transcriber(model_dir_path="models/vosk/modelSmall")

template = """\
ПССМП:
Номер бригады:
Номер карты вызова:
Адрес места вызова:
Пол и возраст больного:
Диагноз основной:
Общая тяжесть состояния:
Уровень сознания по ШКГ:
ЧСС:
АД:
ЧДД:
SpO2:
Температура тела:
Прописка:
Телефон бригады:
Запрос на госпитализацию
"""

dicti = {"id":0}

content_type_mapping = {
    types.ContentType.VOICE: 'voice',
    types.ContentType.AUDIO: 'audio',
    types.ContentType.DOCUMENT: 'document',
}

class FSMHospitalization(StatesGroup):
    substation = State()
    teamNumber = State()
    cardNumber = State()
    # address = State()
    # genderAndAge = State()
    # diagnosis = State()
    # overallConditionSeverity = State()
    # levelOfConsciousness = State()
    # heartRate = State()
    # bloodPressur = State()
    # respiratoryRate  = State()
    # oxygenSaturation  = State()
    # bodyTemperature = State()
    # address = State()
    crewPhone = State()

welcome_message = """\
🏥 <b>Добро пожаловать в InfoMedAssistBot!</b> 🏥

📚 Я - ваш надежный помощник в поиске информации и составлении документов для врачей скорой помощи. 📑

💬 Пожалуйста, воспользуйтесь кнопками ниже, чтобы начать использование бота и получить необходимую помощь. 🤖

🌟 Приятного использования и успешной работы! 🌟
"""

async def command_start(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo="https://wampi.ru/image/Yd23mnl", caption=welcome_message, reply_markup=ikb_client_start)


# async def hospitalization_command(message: types.Message):
#     await FSMHospitalization.substation.set()
#     await message.answer('Введи ПССМП')
#
# @dp.message_handler(content_types=[''])
# async def load_substation(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['substation'] = message.


async def start_page(callback: types.CallbackQuery):
     file = InputMedia(media="https://wampi.ru/image/Yd23mnl", caption=welcome_message)
     await callback.message.edit_media(file, reply_markup=ikb_client_start)
     await callback.answer()

async def main_page(callback: types.CallbackQuery):
     await FSMHospitalization.substation.set()
     result = template.replace("ПССМП:", "<b>ПССМП:</b>")
     file = InputMedia(media="https://postimg.cc/WF6GZYbV", caption=result)
     await callback.message.edit_media(file, reply_markup=ikb_client_main)
     dicti[callback.message.chat.id] = callback.message.message_id
     await callback.answer()


async def algorithms_command(message: types.Message):
    #await message.delete()
    await message.answer('Алгоритмы МОССМП')#, reply_markup=ReplyKeyboardRemove())



async def load_substation(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    async with state.proxy() as data:
        data['substation'] = message.text
    await FSMHospitalization.next()
    result = template.replace("ПССМП:", "ПССМП: " + message.text)
    result = result.replace("Номер бригады:", "<b>Номер бригады:</b>")
    file = InputMedia(media="https://postimg.cc/0rHQngXN", caption=result)
    try:
        await bot.edit_message_media(media=file,chat_id=message.chat.id,message_id=dicti[message.chat.id], reply_markup=ikb_client_main)
    except:
        pass


async def load_teamNumber(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    async with state.proxy() as data:
        data['teamNumber'] = message.text
    await FSMHospitalization.next()
    result = template.replace("Номер бригады:", "Номер бригады: " + message.text)
    result = result.replace("Номер карты вызова:", "<b>Номер карты вызова:</b>")
    file = InputMedia(media="https://postimg.cc/GHmbZXN5", caption=result)
    try:
        await bot.edit_message_media(media=file,chat_id=message.chat.id,message_id=dicti[message.chat.id], reply_markup=ikb_client_main)
    except:
        pass
    


        

# async def echo_bot(message: types.Message):
#     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#     text = message.text
#     result = template.replace("АДРЕС", "АДРЕС: " + text)
#     file = InputMedia(media="https://wampi.ru/image/Yd23mnl", caption=result)
#     try:
#         await bot.edit_message_media(media=file,chat_id=message.chat.id,message_id=dicti[message.chat.id], reply_markup=ikb_client_main)
#     except:
#         pass
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    # await bot.send_photo(chat_id=message.chat.id, photo="https://wampi.ru/image/Yd23mnl", caption=text, reply_markup=ikb_client_start)
    # await message.delete()
    # text = message.text
    # parts = text.split(":")
    # result = parts[1].strip()  # Удаляем лишние пробелы в начале и конце фразы
    # await message.answer(result)

async def speach_to_text(file_id):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        text = await asyncio.to_thread(transcriber.pool_worker, file_on_disk)
    os.remove(file_on_disk)
    return text

async def voice_message(message: types.Message):
    await message.delete()
    if message.content_type in content_type_mapping:
        file_id = getattr(message, content_type_mapping[message.content_type]).file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    # Отправляем начальное сообщение "Расшифровка" и сохраняем его объект
    decryption_message = await message.answer(f"ПССМП: <b>Расшифровка</b>")

    # Создаем объект Event
    decryption_event = asyncio.Event()

    # Запускаем асинхронную функцию для добавления точек
    asyncio.create_task(add_dots_periodically(decryption_message, decryption_event))

    result = await speach_to_text(file_id)
    result = result.capitalize()

    # Устанавливаем Event, чтобы прервать цикл add_dots_periodically
    decryption_event.set()

    # Заменяем сообщение "Расшифровка" на результат расшифровки и добавляем кнопку "Редактировать"
    await decryption_message.edit_text(
        f"<b>ПССМП:</b> {result}",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="✏ Редактировать",
                    switch_inline_query_current_chat=f"\n\n✏ Редактирование:\n\n{result}",
                )
            ]
        ])
    )

async def add_dots_periodically(decryption_message, decryption_event):
    dots = 0
    while not decryption_event.is_set():
        dots = (dots + 1) % 4
        await decryption_message.edit_text(f"ПССМП: <b>Расшифровка</b>" + "<b>.</b>" * dots)
        await asyncio.sleep(1)
    # file = await bot.get_file(file_id)
    # file_path = file.file_path
    # file_on_disk = Path("", f"{file_id}.tmp")
    # await bot.download_file(file_path, destination=file_on_disk)
    # await message.reply("Аудио получено")
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     text = await asyncio.to_thread(transcriber.pool_worker, file_on_disk)
    # # text = await asyncio.get_event_loop().run_in_executor(None, transcriber.pool_worker, file_on_disk)
    # # print(text)
    # await message.answer(f"Вы сказали: {text}")
    # # stt_instance = AsyncSTT()
    # # text = await stt_instance.audio_to_text(file_on_disk)
    # # await message.answer(f"Вы сказали: {text}")
    # elapsed = time.time() - start_time
    # print(elapsed)
    # os.remove(file_on_disk)






def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    # dp.register_message_handler(hospitalization_command, Text(equals="🏥 запрос на госпитализацию", ignore_case=True), state=None)
    # dp.register_message_handler(test_command, content_types=['voice'])
    dp.register_message_handler(load_substation, state=FSMHospitalization.substation)
    dp.register_message_handler(load_teamNumber, state=FSMHospitalization.teamNumber)
    dp.register_message_handler(voice_message, content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
    ])
    dp.register_message_handler(algorithms_command, Text(equals="🧠 алгоритмы моссмп", ignore_case=True))
    dp.register_callback_query_handler(main_page, Text(equals="main_page", ignore_case=True), state=None)
    dp.register_callback_query_handler(start_page, Text(equals="start_page", ignore_case=True))