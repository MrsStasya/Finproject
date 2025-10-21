import os
import aiohttp
import json

# Функция для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Вызов функции для чтения данных из файла .env
load_dotenv()

# Получение токена из переменной окружения, которая была загружена из файла .env
API_YA = os.getenv("API_YA")

#https://api.rasp.yandex.net/v3.0/search/?apikey=37084d0b-8a39-4c53-82aa-439b3230b792&format=json&from=c43&to=c56&lang=ru_RU&page=1&date=2025-09-24&transfers=false
# Функция для парсинга расписания с сайта
async def get_schedule(departure, arrival, date):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.rasp.yandex.net/v3.0/search/?apikey={API_YA}&format=json&from={departure}&to={arrival}&lang=ru_RU&page=1&date={date}&transfers=false") as response:
                #Проверка стутса запроса
                if response.status == 200:
                    print("Все хорошо!Полет нормальный")
                    schedule = await response.json(content_type=None)
                    #Создание директории если ее нет
                    os.makedirs('parse', exist_ok=True)
                    with open('parse/schedule.json', 'w', encoding='utf-8') as file:
                        json.dump(schedule, file, indent=2, ensure_ascii=False)
                else:
                    print(f"Ошибка: {response.status}")
                    raise aiohttp.ClientError(f"HTTP Error: {response.status}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")