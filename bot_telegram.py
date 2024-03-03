from aiogram.utils import executor
from create_bot import dp
from utils.db_api.db_gino import db, on_start
from handlers import client, admin, other

from utils.db_api import quick_commands as commands


async def on_startup(dp):

    print('Настройка хэндлеров')
    client.register_handler_client(dp)
    other.register_handler_other(dp)

    print('Подключение к базе данных')
    await on_start(dp)

    print('Удаление базы данных')
    await db.gino.drop_all()

    print('Создание таблиц')
    await db.gino.create_all()

    print('Бот вышел в онлайн')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)