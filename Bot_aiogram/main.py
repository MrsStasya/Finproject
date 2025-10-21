# Файл написан, чтобы запускать бота и с помощью Router запустить приветствие
# из файла commands

import os
import sys
import asyncio
import logging

# импортируем файл commands.py
import commands

# # импортируем файл parsebase.py - это если будем запускать парсинг сразу с запуском бота постоянно без планировщика
import parse.parsebase as pb

from aiogram import Bot, Dispatcher

# Функция для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Вызов функции для чтения данных из файла .env
load_dotenv()

# Получение токена из переменной окружения, которая была загружена из файла .env
API_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация объекта бота с токеном, который был загружен из переменной окружения
bot = Bot(token=API_TOKEN)

# Создание диспетчера для управления событиями и сообщениями
dp = Dispatcher()

# # Теперь добавляем вызов парсера в начало, чтобы обновить базу данных при запуске бота
# asyncio.create_task(commands.pb.get_base())

async def main():
    try:
        await pb.get_base()
        dp.include_routers(commands.router)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
    # finally:
    #     if commands.scheduler.running: #блок если только планировщик есть
    #         commands.scheduler.shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())