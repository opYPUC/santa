from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.testing.plugin.plugin_base import logging
import logging
from database import crud
import datetime

from database.crud import add_nick

router = Router()


# @router.message(Command("registry"))
# async def select_username_cmd(message:Message):
#    user_id = message.from_user.id
#    if user_id in BUSY_NICKNAMES:
#        await message.reply(f"Ты уже зарегестрирован, твой ник: {BUSY_NICKNAMES[user_id]}")
#        return
#
#    if len(FREE_NICKNAMES) == 0:
#        await message.reply("Ники кончились, попробуй позже")
#        return
#    nickname = FREE_NICKNAMES.pop()
#    BUSY_NICKNAMES[user_id] = nickname


@router.message(Command("addnick"))
async def add_nick_cmd(message: Message, command: CommandObject):
    logging.debug("add_nick_cmd запущен")
    user_id = message.from_user.id
    if not crud.check_adm(user_id):
        await message.reply("У тебя нет прав")
        return
    args = command.args
    argsspl = args.split()
    if args is None:
        await message.reply("Не введен никнейм")
        return
    if (len(argsspl) > 1):
        await message.reply("Ник должен быть одним словом")
        return
    crud.add_nick(args)
    await message.reply("Ник добавлен")


@router.message(Command("registry"))
async def select_username_cmd(message: Message):
    logging.debug("select_username_cmd запущен")
    user_id = message.from_user.id
    if (crud.check_user(user_id)):
        await message.reply(f"Ты уже зарегестрирован, твой id:{user_id}")
        return
    free_nick = crud.get_free_nick()
    if free_nick is None:
        await message.reply(f"Ники кончились, попробуй позже")
        return
    crud.add_user(user_id, free_nick.nick, False, datetime.datetime.now())
    crud.set_owner_id(user_id, free_nick.id)
    await message.reply("Вы зарегестрировались")


@router.message()
async def broadcast_message(message: Message, bot: Bot):
    logging.debug("broadcast запущен")
    if not crud.check_user(message.from_user.id):
        await message.reply("Вы не зарегестрированы")
        return
    users = crud.get_all_users()
    for user in users:
        if user.id == message.from_user.id:
            continue
        data_for_message = f"{user.nickname}" + ': ' + message.text
        await bot.send_message(user.id, data_for_message)
    print(message.from_user.id)
