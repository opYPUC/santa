import asyncio
from loader import dp, bot


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


asyncio.run(main())
