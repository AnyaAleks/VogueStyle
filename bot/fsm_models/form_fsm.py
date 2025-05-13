from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class NewUserForm(StatesGroup):
    phone = State()
    password = State()
    finishing = State()
    
class EnterUserForm(StatesGroup):
    phone = State()
    password = State()