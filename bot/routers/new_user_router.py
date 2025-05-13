from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message
from fsm_models.form_fsm import NewUserForm
from keyboards.agreement_keyboard import agreement_markup
from keyboards.base_keyboard import base_markup
from dto.user_schema import UserSchemaCreate
from services.user_services import _create_user
import asyncio
from main import bot

new_user_router = Router()

@new_user_router.message(F.contact, NewUserForm.phone)
async def capture_phone_name(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.contact.phone_number)
    await state.update_data(name=msg.contact.first_name)
    await state.update_data(tg_id=msg.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=msg.chat.id):
        await asyncio.sleep(1)
        await msg.answer("Отлично теперь напишите пароль для входа: ")
        await state.set_state(NewUserForm.password)
    
@new_user_router.message(F.text, NewUserForm.password)
async def capture_password(msg: Message, state: FSMContext):
    await state.update_data(password=msg.text)
    async with ChatActionSender.typing(bot=bot, chat_id=msg.chat.id):
        await asyncio.sleep(1)
        await msg.answer("Спасибо, что предоставили данные, нажимая кнопку на клавиатру, вы подоставляете разрешение на обработку ваших персональных данных", reply_markup=agreement_markup)
        await state.set_state(NewUserForm.finishing)
    
@new_user_router.message(F.text == "Согласен(а) на обработку персональных данных ✅", NewUserForm.finishing)
async def contact_handler(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    user: UserSchemaCreate = UserSchemaCreate(
        name=user_data["name"],
        tg_id=user_data["tg_id"],
        phone=user_data["phone"],
        password=user_data["password"]
    )
    
    try:
        await _create_user(user)
        await msg.answer("Поздравлняем с присоединением к нам, пожалуйста осмотритесь в нашем меню ниже.", reply_markup=base_markup)
        await state.clear()
    except Exception as e:
        print(e)
        await msg.answer("Произошла ошибка при добавлении вас в БД, обратитесь к администраторам")