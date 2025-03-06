from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from sqlalchemy.testing.plugin.plugin_base import logging
from aiogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
import logging
from database import crud
import datetime



router = Router()

@router.message(CommandStart())
async def select_username_cmd(message: Message):
    logging.debug("start запущен")
    user_id = message.from_user.id
    if (crud.check_user(user_id)):
        await message.reply(f"Ты уже зарегестрирован, твой id:{user_id}")
        return
    crud.add_user(user_id , False, datetime.datetime.now())
    await message.reply("Вы зарегестрировались")


