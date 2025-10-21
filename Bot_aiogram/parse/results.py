#Формирование ссылки url для покупки билетов
from aiogram import types
from datetime import datetime
import json
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#import searchjs
from urllib.parse import quote #для URL кодирования

# Функция для формирования удобного формата даты и времени
def format_datetime(dt):
    dt = datetime.fromisoformat(dt[:-6])
    return dt.strftime('%d.%m.%Y  %H:%M')

#Для всех видов транспорта
async def show_results(message: types.Message, state: FSMContext):
    #Данные из машины состояния
    data = await state.get_data()
    #Открываем файл JSON
    #schedule_data = searchjs.read_json('parse/schedule.json')
    try:
        with open('parse/schedule.json', 'r', encoding='utf-8') as file:
            schedule_data = json.load(file)
            for segments in schedule_data['segments']:
                departure_date = format_datetime(segments['departure'])  # формирование даты и времени отправления
                arrival_date = format_datetime(segments['arrival'])  # формирование даты и времени прибытия
                transport_types = segments['thread']['transport_type']
                departure = segments['from']['title']
                arrival = segments['to']['title']
                # Формируем корректную дату для URL
                formatted_departure = datetime.fromisoformat(segments['departure'][:-6]).strftime('%Y-%m-%dT%H:%M:%S')
                # Формируем URL с корректными параметрами
                # url = (
                #     f"https://travel.yandex.ru/{quote(transport_types)}?"
                #     f"from={quote(departure)}&"
                #     f"to={quote(arrival)}&"
                #     f"departure={formatted_departure}&"
                #     f"adults=1"
                # )
                message_text = (
                    f"Пункт отправления: {segments['from']['title']}\n"
                    f"Дата и время отправления: {departure_date}\n"
                    f"Пункт прибытия: {segments['to']['title']}\n"
                    f"Дата и время прибытия: {arrival_date}\n"
                    f"Вид транспорта: {segments['thread']['transport_type']}\n"
                    f"Номер рейса: {segments['thread']['number']}\n"
                    f"Перевозчик: {segments['thread']['carrier']['title']}\n"
                    # f"Стоимость: {segments['thread']['tickets_info']['places']['price']}\n"
                    # f"Наличие мест: {segments['thread']['tickets_info']['places']['name']}\n"
                )
                # Инфо о билетах и стоимости
                if 'tickets_info' in segments['thread'] and segments['thread']['tickets_info'].get('places'):
                    places = segments['thread']['tickets_info']['places']
                    if places:
                        for place in places:
                            message_text += (f"Стоимость билета: {place['price']['whole']}.{place['price']['cents']}\n"
                                             f"Места доступны\n"
                                             )
                    else:
                        message_text += "Билеты недоступны\n"
                else:
                    message_text += "Информация о наличии мест и стоимости билетов недоступна\n"
                # Создаем клавиатуру с кнопкой
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Купить билет", url="https://travel.yandex.ru/")]
                    ]
                )
                # Отправляем сообщение с клавиатурой
                await message.answer(message_text, reply_markup=keyboard)

    except FileNotFoundError:
        print(f"Файл schedule.json не найден")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в schedule.json")
        return None

async def show_results_transport_type(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        with open('parse/schedule.json', 'r', encoding='utf-8') as file:
            schedule_data = json.load(file)
            found_matches = False  # Флаг для отслеживания найденных рейсов

            for segments in schedule_data['segments']:
                if data["transport_type"] == segments['thread']['transport_type']:
                    found_matches = True  # Устанавливаем флаг, если нашли подходящий рейс

                    departure_date = format_datetime(segments['departure'])
                    arrival_date = format_datetime(segments['arrival'])
                    transport_types = segments['thread']['transport_type']
                    departure = segments['from']['title']
                    arrival = segments['to']['title']
                    # Формируем корректную дату для URL
                    formatted_departure = datetime.fromisoformat(segments['departure'][:-6]).strftime(
                        '%Y-%m-%dT%H:%M:%S')
                    # Формируем URL с корректными параметрами
                    # url = (
                    #     f"https://travel.yandex.ru/{quote(transport_types)}?"
                    #     f"from={quote(departure)}&"
                    #     f"to={quote(arrival)}&"
                    #     f"departure={formatted_departure}&"
                    #     f"adults=1"
                    # )
                    message_text = (
                        f"Пункт отправления: {segments['from']['title']}\n"
                        f"Дата и время отправления: {departure_date}\n"
                        f"Пункт прибытия: {segments['to']['title']}\n"
                        f"Дата и время прибытия: {arrival_date}\n"
                        f"Вид транспорта: {segments['thread']['transport_type']}\n"
                        f"Номер рейса: {segments['thread']['number']}\n"
                        f"Перевозчик: {segments['thread']['carrier']['title']}\n"

                    )

                    if 'tickets_info' in segments['thread'] and segments['thread']['tickets_info'].get('places'):
                        places = segments['thread']['tickets_info']['places']
                        if places:
                            for place in places:
                                message_text += (
                                    f"Стоимость билета: {place['price']['whole']}.{place['price']['cents']}\n"
                                    f"Места доступны\n"
                                    )
                        else:
                            message_text += "Билеты недоступны\n"
                    else:
                        message_text += "Информация о наличии мест и стоимости билетов недоступна\n"
                    #Клавиатура
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text="Купить билет", url="https://travel.yandex.ru/")]
                        ]
                    )
                    await message.answer(message_text, reply_markup=keyboard)

            # Если не найдено ни одного подходящего рейса
            if not found_matches:
                await message.answer(f"На выбранную дату данный вид транспорта: {data['transport_type']} недоступен")

    except FileNotFoundError:
        print(f"Файл schedule.json не найден")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в schedule.json")
        return None






# async def form_url(transport_type, departure, arrival, date):
#     url = "https://travel.yandex.ru/{transport_type}?from={departure}&to={arrival}&departure={date}&adults=1"
#     return url

# async def results():
#     data = searchjs.read_json('parse/schedule.json')
#     schedule = []
#     try:
#         for segment in data("countries", []):
#             for region in country.get("regions", []):
#                 for settlement in region.get("settlements", []):
#                     if search_word.lower() in settlement["title"].lower():
#                         print(settlement)
#                         found_results.append(settlement)  # Добавляем найденный объект в список
#         if not found_results:
#             print("Станция не найдена")
#         return found_results  # Возвращаем список найденных результатов
#     except KeyError as e:
#         print(f"Ошибка в структуре JSON: отсутствует ключ {e}")
#         return []
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return []




