from aiogram import Bot, Dispatcher
from handlers import test_handler
import logging
from database_old import database_old
from dotenv import load_dotenv
import os

load_dotenv() #загружаем из .env загружаем в терминал переменные

logging.basicConfig(level=logging.INFO)


bot = Bot(token=os.getenv("TOKEN","***"))
dp = Dispatcher()


dp.include_routers(test_handler.router)