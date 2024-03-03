from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

storage=MemoryStorage()

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")

dp = Dispatcher(bot, storage=storage)

