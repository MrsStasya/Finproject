import json
import os

#Функция чтения json файла
def read_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в {filename}")
        return None

#Функция сохранения результатов для departure - НЕНУЖНО
async def save_search_result_departure(data):
    try:
        os.makedirs('parse', exist_ok=True)
        with open('parse/departure.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print('Результаты поиска сохранены в файл departure.json')
    except Exception as e:
        print(f"Ошибка присохранении файла: {e}")

#Функция сохранения результатов для arrival - НЕНУЖНО
async def save_search_result_arrival(data):
    try:
        os.makedirs('parse', exist_ok=True)
        with open('parse/arrival.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print('Результаты поиска сохранены в файл arrival.json')
    except Exception as e:
        print(f"Ошибка присохранении файла: {e}")


# Функция поиска по json файлу, пока неизвестен вид транспорта.
# При выборе варианта all types код нужен будет именно населенного пункта(города).
# Функция работает конкретно с базой base.json
async def find_json(search_word):
    data = read_json('parse/base.json') #Тут нужен абсолютный путь с указанием папки для работы из main. Если тестируем часть, то убирать абс путь
    found_results = []  # Список для хранения найденных результатов
    try:
        for country in data.get("countries", []):
            for region in country.get("regions", []):
                for settlement in region.get("settlements", []):
                    if search_word.lower() in settlement["title"].lower():
                        print(settlement)
                        found_results.append(settlement)  # Добавляем найденный объект в список
        if not found_results:
            print("Станция не найдена")
        return found_results  # Возвращаем список найденных результатов
    except KeyError as e:
        print(f"Ошибка в структуре JSON: отсутствует ключ {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

#Функция для извлечения кода при выборе всех видов транспорта
async def transport_type_all(result):
    try:
        yandex_code = None
        for settlement in result:
            if 'codes' in settlement:
                code_data = settlement['codes']
                if isinstance(code_data, dict) and 'yandex_code' in code_data:
                    yandex_code = code_data['yandex_code']
                    break
        if yandex_code is None:
            print('yandex_code не найден!')
        return yandex_code
    except Exception as e:
        print(f"Ошибка при поиске yandex_code: {e}")
        return e

#Функция для извлечения кода при выборе определенного вида транспорта - не нужно
async def transport_type_departure(transport_type):
    data = read_json('parse/departure.json')#абсолютный путь убираем при тестировании в этом файле
    ya_code_departure = None
    try:
        for stations in data.get("stations", []):
            for transport_type in stations.get("transport_type", []):
                if transport_type.lower() in transport_type["transport_type"].lower():
                    ya_code_departure = stations.codes.yandex_code
                    print(ya_code_departure)
                    return ya_code_departure  # Возвращаем список найденных результатов
    except KeyError as e:
        print(f"Ошибка в структуре JSON: отсутствует ключ {e}")
        return e
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return e
#Проверка работы блока
# async def work_js():
#     try:
#         search_word = "Казань"
#         results = await find_json(search_word)
#         ya_code = await transport_type_all(results)
#         print("Найденный ya_code:", ya_code)
#         return ya_code
#     except Exception as e:
#         print(f"Произошла ошибка в работе с JSON: {e}")
#
#
#
# import asyncio
# async def main():
#     await work_js()
# if __name__ == "__main__":
#     asyncio.run(main())


