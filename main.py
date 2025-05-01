import asyncio
import os
import logging

from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher

from handlers import router

from dotenv import load_dotenv


logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщений
    handlers=[
        RotatingFileHandler("bot.log", maxBytes=5 * 1024 * 1024, backupCount=2),  # Логи в файл (5 МБ на файл, 2 бэкапа)
        logging.StreamHandler()  # Логи в консоль
    ]
)

logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    bot = Bot(token = os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('***EXIT***')