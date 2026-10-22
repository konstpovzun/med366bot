import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, symptoms, analysis, fallback, link_handler, fact_handler, photo_handler, video_handler

from keep_alive import keep_alive
keep_alive()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(symptoms.router)
dp.include_router(analysis.router)
dp.include_router(link_handler.router)
dp.include_router(fact_handler.router)
dp.include_router(photo_handler.router)
dp.include_router(video_handler.router) # НОВЫЙ РОУТЕР
dp.include_router(fallback.router)


async def main():
    logging.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")