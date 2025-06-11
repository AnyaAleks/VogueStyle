import logging
import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.filters import CommandStart
from aiogram import F
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
load_dotenv()
# Токен бота и базовый URL API
TOKEN = getenv("BOT_TOKEN")
API_URL = "http://backend:8000"

# Инициализация Dispatcher
dp = Dispatcher()

# --- Обработчик команды /start ---
@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработка команды /start:
    - Если пользователь является мастером (role=2), показываем клавиатуру.
    - Если обычный, проверяем в базе по tg_id. Если не найден — просим обратиться к администратору.
      Если найден — показываем клавиатуру.
    """
    user_id = message.from_user.id

    # 1. Проверяем, есть ли пользователь среди мастеров (role 2)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/tg/all/2") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    masters = data.get("tgs", []) if data.get("ok") else []
                else:
                    await message.answer("Сервис мастеров временно недоступен. Попробуйте позже.")
                    return
    except Exception as e:
        logging.error(f"Ошибка при запросе /tg/all/2: {e}")
        await message.answer("Ошибка при обращении к сервису мастеров.")
        return

    is_master = str(user_id) in [str(tg_id) for tg_id in masters]

    if not is_master:
        # 2. Если не мастер — проверяем обычного пользователя в базе по tg_id
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_URL}/user/tg_id/{user_id}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        user = data.get("user")
                    elif resp.status == 404:
                        await message.answer("Вы не зарегистрированы. Пожалуйста, обратитесь к администратору.")
                        return
                    else:
                        await message.answer("Сервис пользователей временно недоступен. Попробуйте позже.")
                        return
        except Exception as e:
            logging.error(f"Ошибка при запросе /user/tg_id/{user_id}: {e}")
            await message.answer("Ошибка при обращении к сервису пользователей.")
            return

    # 3. Собираем и отправляем клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записаться"), KeyboardButton(text="Список мастеров")]
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)


# --- Обработчик кнопки "Список мастеров" ---
@dp.message(F.text == "Список мастеров")
async def list_masters_handler(message: Message):
    """
    Обработка команды/кнопки "Список мастеров":
    Получаем список мастеров через GET /master и выводим информацию по каждому.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/master") as resp:
                if resp.status == 200:
                    masters = await resp.json()
                else:
                    await message.answer("Сервис мастеров временно недоступен. Попробуйте позже.")
                    return
    except Exception as e:
        logging.error(f"Ошибка при запросе /master: {e}")
        await message.answer("Ошибка при получении списка мастеров.")
        return

    if not isinstance(masters, list) or len(masters) == 0:
        await message.answer("Список мастеров пуст.")
        return

    for master in masters:
        master_id = master.get("id")
        name = master.get("name", "Без имени")
        position = master.get("job", "Не указано")
        experience = master.get("experience", "Не указан")
        email = master.get("email", "Не указан")
        photo_url = master.get("photo_link")

        caption = (
            f"<b>{name}</b>\n"
            f"Должность: {position}\n"
            f"Опыт: {experience}\n"
            f"Email: {email}"
        )

        # Inline-клавиатура с кнопками "Записаться" и "Услуги"
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Записаться", callback_data=f"signup:{master_id}"),
                    InlineKeyboardButton(text="Услуги", callback_data=f"services:{master_id}"),
                ]
            ]
        )

        try:
            if photo_url:
                # Если есть ссылка на фото — отправляем как photo
                await message.answer_photo(photo=photo_url, caption=caption, reply_markup=inline_kb)
            else:
                # Если фото нет — отправляем текст
                await message.answer(caption, reply_markup=inline_kb)
        except Exception as e:
            logging.error(f"Ошибка при отправке данных мастера: {e}")
            await message.answer(caption, reply_markup=inline_kb)


# --- Callback: показать услуги мастера ---
@dp.callback_query(F.data.startswith("services:"))
async def services_callback(callback: CallbackQuery):
    """
    Обработка нажатия inline-кнопки "Услуги":
    Показывает список услуг выбранного мастера.
    """
    await callback.answer()  # Скрыть индикатор загрузки на кнопке

    master_id = callback.data.split(":")[1]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/master") as resp:
                if resp.status == 200:
                    masters = await resp.json()
                else:
                    await callback.message.answer("Не удалось получить данные мастеров.")
                    return
    except Exception as e:
        logging.error(f"Ошибка при запросе /master для услуг: {e}")
        await callback.message.answer("Ошибка при обращении к сервису мастеров.")
        return

    # Находим нужного мастера
    target = None
    for m in masters:
        if str(m.get("id")) == master_id:
            target = m
            break

    if not target:
        await callback.message.answer("Мастер не найден.")
        return

    services = target.get("services", [])
    if not services:
        await callback.message.answer("У данного мастера нет услуг.")
    else:
        text = "<b>Услуги мастера:</b>\n"
        for svc in services:
            # Предполагаем, что в каждом объекте услуги есть поля name, price, duration
            name = svc.get("name", "—")
            price = svc.get("price", "—")
            duration = svc.get("duration", "—")
            text += f"• {name} — {price}₽ ({duration} мин)\n"
        await callback.message.answer(text, parse_mode=ParseMode.HTML)


# --- Callback: заглушка "Записаться" ---
@dp.callback_query(F.data.startswith("signup:"))
async def signup_callback(callback: CallbackQuery):
    """
    Обработка нажатия inline-кнопки "Записаться" (заглушка).
    """
    await callback.answer("Функция \"Записаться\" пока недоступна.", show_alert=True)


# --- Запуск бота ---
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
