from aiogram.fsm.state import StatesGroup, State


class Employ(StatesGroup):
    telegram_id = State()
    first_name = State()
    last_name = State()
    phone = State()
