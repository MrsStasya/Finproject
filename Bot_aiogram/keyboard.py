# подключение библиотек для создания инлайн кнопок
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создаем кнопку "Старт"
start_button = InlineKeyboardButton(
    text="Старт",
    callback_data="start_bot"
)

keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[[start_button]]
)

#Клавиатура для начального сообщения
def inline_kb():
    inline_kb = [
        [InlineKeyboardButton(text='Поехали!', callback_data='letsgo')],
        [InlineKeyboardButton(text='Закончить!', callback_data='end')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

# Клавиатура для выбора вида транспорта
def transport_types():
    transport_kb = [
        [InlineKeyboardButton(text='Все виды транспорта', callback_data='all')],
        [InlineKeyboardButton(text='Самолет', callback_data='plane')],
        [InlineKeyboardButton(text='Поезд', callback_data='train')],
        [InlineKeyboardButton(text='Электричка', callback_data='suburban')],
        [InlineKeyboardButton(text='Автобус', callback_data='bus')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=transport_kb, resize_keyboard=True)

#Клавиатура для ссылками на бронирование билетов с сайта яндекс.путешествия
def buy_tickets():
    tickets = [
        [InlineKeyboardButton(text='Купить билет', url='')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=tickets, resize_keyboard=True)
# # Создание клавиатуры для ввода станции отправления
# def st_departure():
#     departure_kb = [
#         [KeyboardButton(text="Поделиться геопозицией", request_location=True)],
#         [KeyboardButton(text="Ввести станцию отправления вручную", request_chat=None)]
#     ]
#     return ReplyKeyboardMarkup(keyboard=departure_kb, resize_keyboard=True, one_time_keyboard=True)