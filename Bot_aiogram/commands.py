# Используем Routers, чтобы запускать код отсюда в файле main.py

from aiogram import types, Router, F

from aiogram.filters import CommandStart

from aiogram.types import CallbackQuery

#  Импортируем FSM - машина состояний И FSMContext(для управления состояниями)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime, timezone, timedelta
import re
import keyboard as kb

#Это строка нужна если мы планировщик запускаем в этом блоке при старте. Пока не нужна
# import parse.parsebase as pb

import parse.searchjs
import parse.parseway
import parse.results
# #Импорт планировщик
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()

# # #Создаем планировщик
# scheduler = AsyncIOScheduler()

# Создаем дочерник к StatesGroup класс
class Info(StatesGroup):
    departure = State()
    arrival = State()
    date = State()
    transport_type = State()

@router.message(CommandStart())
async def welcome_message(message: types.Message):
    await message.answer("Здравствуйте!"
                         "\n" ""
                         "\nЯ - Ваш персональный помощник для поиска билетов на Яндекс.Расписание."
                         "\n"
                         "\nДля  начала работы необходимо указать начальный пункт отправления."
                         "\n"
                         "\nИспользуя бот, Вы даете согласие на обработку персональных данных и определение Вашего местоположения."
                         "\n"
                         "Нажмите кнопку 'Поехали!', если желаете искать билеты(убедитесь, что определение Вашей геопозиции включено или кнопку 'Закончить!' для завершения работы".center(
        100), reply_markup=kb.inline_kb())

# Ответы на кнопки при старте
@router.callback_query(F.data == "letsgo")
async def start_work(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.departure)
    await callback.message.answer("Введите пункт отправления", show_alert=True)

@router.message(Info.departure)
async def step_two(message: types.Message, state: FSMContext):
    departure = await parse.searchjs.find_json(message.text.strip().lower())
    if not departure:
        await message.answer("Станция отправления не найдена в базе данных.\n "
                             "Введите другой название")
        return
    #await parse.searchjs.save_search_result_departure(departure) #Это для сохранения результата поиска в файл. Не нужно
    await state.update_data(departure=message.text)
    await state.set_state(Info.arrival)
    await message.answer('Введите пункт назначения')

@router.message(Info.arrival)
async def step_three(message: types.Message, state: FSMContext):
    arrival = await parse.searchjs.find_json(message.text.strip().lower())
    #await parse.searchjs.save_search_result_arrival(arrival) #Это для сохранения результата поиска в файл. Не нужно
    if not arrival:
        await message.answer("Станция прибытия не найдена в базе данных.\n "
                             "Введите другой название")
        return
    await state.update_data(arrival=message.text)
    await state.set_state(Info.date)
    await message.answer('Введите дату вашего путешествия в формате число.месяц.год')

@router.message(Info.date)
async def step_four(message: types.Message, state: FSMContext):
    user_date = message.text.strip()
    date_rule = r'^\d{2}\.\d{2}\.\d{4}$'
    if re.match(date_rule, user_date):
        try:
            parsed_date = datetime.strptime(user_date, '%d.%m.%Y')
            await state.update_data(date=user_date)
            data = await state.get_data()
            departure = await parse.searchjs.find_json(data["departure"])
            arrival = await parse.searchjs.find_json(data["arrival"])
            ya_code_departure = await parse.searchjs.transport_type_all(departure)
            ya_code_arrival = await parse.searchjs.transport_type_all(arrival)
            format_data = parsed_date.strftime('%Y-%m-%d')
            await parse.parseway.get_schedule(ya_code_departure, ya_code_arrival, format_data)
            await state.set_state(Info.transport_type)
            await message.answer('Выберите необходимый вид транспорта', reply_markup=kb.transport_types())
        except ValueError:
            await message.answer("Некорректная дата! Введите дату в формате ДД.ММ.ГГГГ")
    else:
        await message.answer(
            'Неверный формат даты!\n'
            'Пожалуйста, введите дату в формате ДД.ММ.ГГГГ'
        )

@router.callback_query(F.data == "all")
async def transport_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.transport_type)
    await state.update_data(transport_type="all")
    info = await state.get_data()
    await callback.message.answer(f'Вы ввели следующие данные.\nПункт отправления: {info["departure"]}\nПункт назначения: {info["arrival"]}\nДата путешемтвия: {info["date"]}\nВид транспорта: {info["transport_type"]}')
    await parse.results.show_results(callback.message, state)
    await state.clear()

@router.callback_query(F.data == "plane")
async def transport_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.transport_type)
    await state.update_data(transport_type="plane")
    info = await state.get_data()
    await callback.message.answer(f'Вы ввели следующие данные.\nПункт отправления: {info["departure"]}\nПункт назначения: {info["arrival"]}\nДата путешемтвия: {info["date"]}\nВид транспорта: {info["transport_type"]}')
    await parse.results.show_results_transport_type(callback.message, state)
    await state.clear()

@router.callback_query(F.data == "train")
async def transport_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.transport_type)
    await state.update_data(transport_type="train")
    info = await state.get_data()
    await callback.message.answer(f'Вы ввели следующие данные.\nПункт отправления: {info["departure"]}\nПункт назначения: {info["arrival"]}\nДата путешемтвия: {info["date"]}\nВид транспорта: {info["transport_type"]}')
    await parse.results.show_results_transport_type(callback.message, state)
    await state.clear()


@router.callback_query(F.data == "suburban")
async def transport_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.transport_type)
    await state.update_data(transport_type="suburban")
    info = await state.get_data()
    await callback.message.answer(f'Вы ввели следующие данные.\nПункт отправления: {info["departure"]}\nПункт назначения: {info["arrival"]}\nДата путешемтвия: {info["date"]}\nВид транспорта: {info["transport_type"]}')
    await parse.results.show_results_transport_type(callback.message, state)
    await state.clear()

@router.callback_query(F.data == "bus")
async def transport_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Info.transport_type)
    await state.update_data(transport_type="bus")
    info = await state.get_data()
    await callback.message.answer(f'Вы ввели следующие данные.\nПункт отправления: {info["departure"]}\nПункт назначения: {info["arrival"]}\nДата путешемтвия: {info["date"]}\nВид транспорта: {info["transport_type"]}')
    await parse.results.show_results_transport_type(callback.message, state)
    await state.clear()

@router.callback_query(F.data == "end")
async def end_work(callback: types.CallbackQuery):
    await callback.message.answer("Как жаль, что Вы уходите! \nДо новых встреч!", show_alert=True)

