import asyncio
from loader import dp, bot
from utils.main_menu import set_bot_comands

async def main():
    print("Бот запущен")
    await set_bot_comands(bot)
    await dp.start_polling(bot)




asyncio.run(main())
