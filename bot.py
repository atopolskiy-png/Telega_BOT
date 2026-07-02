import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

# ❗ ВАЖНО: принудительно импортируем модули handlers
import handlers.start
import handlers.admin

from handlers.start import router as start_router
from handlers.admin import router as admin_router


async def main():

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # =========================
    # Подключаем роутеры
    # =========================

    dp.include_router(start_router)
    dp.include_router(admin_router)

    print("🏒 Golden Hawks bot запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())