from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Предоставить номер телефона', request_contact=True)]
])