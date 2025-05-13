from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from fsm_models.form_fsm import NewUserForm, EnterUserForm
from keyboards.base_keyboard import base_markup
from keyboards.contact_keyboard import contact_markup
from keyboards.new_or_link_keyboard import new_or_link_markup
from dto.user_schema import UserSchemaGet, UserSchemaCreate
from services.user_services import _get_user_by_tg_id

start_router = Router()

@start_router.message(CommandStart())
async def start_handler(msg: Message):
    user: UserSchemaGet = await _get_user_by_tg_id(msg.from_user.id)
    if user is None:
        await msg.answer("Добро пожаловать в VogueStyle!\nВаш Telegram-аккаунт не найден в нашей базе, пожалуйста создайте новый аккаунт или свяжите Telegram-аккаунт с аккаунтов на сайте", 
                         reply_markup=new_or_link_markup)
    else:
        await msg.answer("Ваш аккаунт уже был зарегистрирован у нас, приятного использования!", reply_markup=base_markup)

@start_router.message(F.text == "Создать аккаунт")
async def new_account_handler(msg: Message, state: FSMContext):
    await msg.answer("Предоставьте пожалуйста данные о номере телефона с помощью кнопки ниже", reply_markup=contact_markup)
    await state.set_state(NewUserForm.phone)
    
@start_router.message(F.text == "Связать аккаунты")
async def link_account_handler(msg: Message, state: FSMContext):
    await msg.answer("Предоставьте пожалуйста данные о номере телефона с помощью кнопки ниже", reply_markup=contact_markup)
    await state.set_state(EnterUserForm.phone)
