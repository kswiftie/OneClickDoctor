from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


CITIES = ['Санкт-Петербург',]
SPECIALTIES = ['Терапевт', 'Кардиолог', 'Невролог']


def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='ℹ️ Инфа', callback_data='info')],
            [InlineKeyboardButton(
                text='🩺 Подобрать врача', callback_data='find_doctor')],
            [InlineKeyboardButton(
                text='💬 Помочь с симптомами', callback_data='chat')],
        ]
    )


def menu_button(from_info=False):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text='🏠 В меню',
            callback_data='to_menu_from_info' if from_info else 'to_menu'
        )]]
    )


def get_city_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=city,
                callback_data=f'doctor_city_{city}'
            ) for city in CITIES],
            [InlineKeyboardButton(
                text='🏠 В меню',
                callback_data='to_menu_from_doctor_search'
            )]
        ]
    )


def get_specialty_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=spec,
                callback_data=f'doctor_spec_{spec}'
            ) for spec in SPECIALTIES],
            [InlineKeyboardButton(
                text='🏠 В меню',
                callback_data='to_menu_from_doctor_search'
            )]
        ]
    )
