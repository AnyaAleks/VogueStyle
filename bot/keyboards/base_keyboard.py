from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Записаться')],
    [KeyboardButton(text='Список мастеров'), KeyboardButton(text='История посещений')]
], resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню ниже \/')