from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_comands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Регистрация"),
        BotCommand(command="join_room", description="Присоедениться к комнате"),
        BotCommand(command="create_room", description="Создать комнату"),
        BotCommand(command="leave_room", description="Покинуть комнату")
    ])
