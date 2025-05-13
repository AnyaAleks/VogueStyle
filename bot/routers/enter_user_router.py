from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from fsm_models.form_fsm import EnterUserForm
from services.user_services import _check_user, _link_user
from dto.user_schema import UserSchemaCheck, UserSchemaLink
from keyboards.base_keyboard import base_markup

enter_user_router = Router()

@enter_user_router.message(F.contact, EnterUserForm.phone)
async def capture_phone(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.contact.phone_number)
    await msg.answer("Отлично теперь напишите пароль для входа: ")
    await state.set_state(EnterUserForm.password)
        
@enter_user_router.message(F.text, EnterUserForm.password)
async def capture_password(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    logged_data = await _check_user(UserSchemaCheck(phone=state_data["phone"], password=msg.text))
    if logged_data["ok"]:
        await _link_user(UserSchemaLink(id=logged_data["user"]["id"], tg_id=msg.from_user.id))
        await msg.answer("Вы успешно связали аккаунты, теперь можете пользоваться Telegram ботом!", reply_markup=base_markup)
    else:
        await msg.answer("Произошла ошибка при попытке свзяать аккаунты")