from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_or_link_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать аккаунт')],
    [KeyboardButton(text='Связать аккаунты')]
], resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню ниже \/')