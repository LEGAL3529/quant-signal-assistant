import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.equity import equity_handler

# Вставь сюда свой токен
BOT_TOKEN = os.getenv("7947328586:AAGhTyJ8bSMU0BrfcXrIPx9SFjjjjjjjjjj") or "YOUR_TELEGRAM_BOT_TOKEN"

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Хендлер обёртка (aiogram 3 — нужен Dispatcher)
async def on_startup(bot: Bot) -> None:
    logging.info("Бот запущен")

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем команду /equity
    dp.message.register(equity_handler, commands={"equity"})

    # Запуск
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())
