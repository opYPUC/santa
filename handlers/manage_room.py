from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from database import crud
import logging

router = Router()

EXAMPLE_COMMAND = "(/create_room назв. пар.)"

@router.message(Command("create_room"))
async def create_room_cmd(message: Message, command: CommandObject):
   logging.debug("create_room запущена")
   if crud.check_owner_id_room(message.from_user.id):
      await message.reply("Ты уже состоишь в комнате")
      return
   args = command.args
   if args is None:
      await message.reply("Не введены параметры комнаты"
                          f"{EXAMPLE_COMMAND}")
      return
   args = args.split(" ")
   if (len(args) != 2):
      await message.reply("Комната имеет только 2 параметра"
                          f"{EXAMPLE_COMMAND}")
      return
   crud.create_room(args[0],
                    args[1],
                    message.from_user.id)
   await message.reply("Комната создана")


