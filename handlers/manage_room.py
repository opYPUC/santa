from aiogram import Router, Bot
from aiogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.filters import Command, CommandObject
from aiohttp.web_fileresponse import content_type

from database import crud
import logging
from utils.states import InputRoomData
from aiogram.fsm.context import FSMContext
import hashlib

router = Router()

EXAMPLE_COMMAND = "(назв. пар.)"


@router.message(Command("create_room"))
async def create_room_cmd(message: Message, command: CommandObject, state:FSMContext):
   logging.debug("create_room запущена")
   if not crud.is_user_registered(message.from_user.id):
       await message.reply("Сначала зарегистрируйтесь(/start)")
       return
   if crud.check_room_id(message.from_user.id):
      await message.reply("Ты уже состоишь в комнате")
      return
   await message.reply("Введите аргументы")
   await state.set_state(InputRoomData.input_data.state)
   await state.set_data({"action":"create"})

   #args = command.args
   #if args is None:
   #   await message.reply("Не введены параметры комнаты"
   #                       f"{EXAMPLE_COMMAND}")
   #   return
   #args = args.split(" ")
   #if (len(args) != 2):
   #   await message.reply("Комната имеет только 2 параметра"
   #                       f"{EXAMPLE_COMMAND}")
   #   return
   #crud.create_room(args[0],
   #                 args[1],
   #                 message.from_user.id)
   #await message.reply("Комната создана")

#@router.message(Command("create_room"))
#async def create_room_cmd(message: Message, command: CommandObject, state:FSMContext):
#   logging.debug("create_room запущена")
#   if crud.check_owner_id_room(message.from_user.id):
#      await message.reply("Ты уже состоишь в комнате")
#      return
#   await InputRoomData.input_data.set()
#   data = await state.get_data()
#   room_name = data.get("room_name")
#   password = data.get("password")
#   crud.create_room(room_name,
#                    password,
#                    message.from_user.id)

@router.message(InputRoomData.input_data)
async def input_args(message: Message,state: FSMContext):
    is_create = (await state.get_data()).get("action","") == "create"
    print(state.get_state())
    try:
        room_name,password = message.text.split()
    except ValueError:
        await message.reply(f"Пожалуйста, отправьте данные в формате: {EXAMPLE_COMMAND}")
        return
    if is_create and crud.check_busy_name_room(room_name):
        await message.reply("Комната с таким названием уже существует, попробуйте другое название")
        return
    if is_create:
        crud.create_room(room_name, password, message.from_user.id)
    else:
        if not crud.check_valid_room(room_name, password):
            await message.reply("Неверное название или пароль, попробуйте заново")
            return
        crud.join_room(message.from_user.id, room_name)
    await message.reply(f"Название комнаты: {room_name}\nПароль: {password}")
    if is_create:
        await message.reply("Комната создана")
    else:
        await message.reply("Успешный вход")
    await state.clear()

@router.message(Command("leave_room"))
async def create_room_cmd(message: Message, command: CommandObject):
    logging.debug("leave_room запущена")
    if not crud.is_user_registered(message.from_user.id):
        await message.reply("Сначала зарегистрируйтесь(/start)")
        return
    if not crud.check_user_id_room(message.from_user.id):
        await message.reply("Ты и так не состоишь в комнате")
        return
    crud.delete_room_from_user(message.from_user.id)
    await message.reply("Пользователь покинул комнату")

@router.message(Command("join_room"))
async def create_room_cmd(message: Message, command: CommandObject,state:FSMContext):
    logging.debug("join_room запущена")
    if not crud.is_user_registered(message.from_user.id):
        await message.reply("Сначала зарегистрируйтесь(/start)")
        return
    if crud.check_user_id_room(message.from_user.id):
        await message.reply("Ты уже состоишь в комнате")
        return
    await message.reply("Введите аргументы")
    await state.set_state(InputRoomData.input_data.state)
    await state.set_data({"action": "join"})

    #args = command.args
    #if args is None:
    #    await message.reply("Не введены параметры комнаты"
    #                        f"{EXAMPLE_COMMAND}")
    #    return
    #args = args.split(" ")
    #if (len(args) != 2):
    #    await message.reply("Комната имеет только 2 параметра"
    #                        f"{EXAMPLE_COMMAND}")
    #    return
    #if not crud.check_valid_room(args[0], args[1]):
    #    await message.reply("Неверное имя комнаты или пароль")
    #    return
    #crud.join_room(message.from_user.id, args[0])
    #await message.reply("Присоединение...")

