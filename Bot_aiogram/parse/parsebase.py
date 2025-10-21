import os
import aiohttp
import json

# Функция для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Вызов функции для чтения данных из файла .env
load_dotenv()

# Получение токена из переменной окружения, которая была загружена из файла .env
API_YA = os.getenv("API_YA")

#https://api.rasp.yandex-net.ru/v3.0/stations_list/?apikey=37084d0b-8a39-4c53-82aa-439b3230b792
#https://api.rasp.yandex.net/v3.0/stations_list/?apikey=37084d0b-8a39-4c53-82aa-439b3230b792


async def get_base():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.rasp.yandex-net.ru/v3.0/stations_list/?apikey={API_YA}&lang=ru_RU&format=json") as response:
                #Проверка стутса запроса
                if response.status == 200:
                    print("Запрос прошел успешно! Данные получены")
                    base = await response.json(content_type=None)
                    #Создание директории если ее нет
                    os.makedirs('parse', exist_ok=True)
                    with open('parse/base.json', 'w', encoding='utf-8') as file:
                        json.dump(base, file, indent=2, ensure_ascii=False)
                else:
                    print(f"Ошибка: {response.status}")
                    raise aiohttp.ClientError(f"HTTP Error: {response.status}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

