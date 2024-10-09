from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from database import crud
import datetime

router = Router()

#@router.message(Command("registry"))
#async def select_username_cmd(message:Message):
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

@router.message(Command("registry"))
async def select_username_cmd(message:Message):
    user_id = message.from_user.id
    if (crud.check_user(user_id)):
        await message.reply(f"Ты уже зарегестрирован, твой id:{user_id}")
        return
    free_nick = crud.get_free_nick()
    if free_nick is None:
        await message.reply(f"Ники кончились, попробуй позже")
        return
    crud.add_user(user_id,free_nick.nick,False,datetime.datetime.now())
    await message.reply("Вы зарегестрировались")


@router.message()
async def broadcast_message(message: Message, bot: Bot):
    if not crud.check_user(message.from_user.id):
        await message.reply("Вы не зарегестрированы")
        return
    users = crud.get_all_users()
    for user in users:
        if user.id == message.from_user.id:
            continue
        data_for_message = f"{user.nickname}"+': '+message.text
        await bot.send_message(user.id, data_for_message)
    print(message.from_user.id)




