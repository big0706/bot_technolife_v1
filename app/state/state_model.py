from aiogram.fsm.state import StatesGroup, State


class Employ(StatesGroup):
    telegram_id = State()
    name = State()
    surname = State()
    username = State()
    phone = State()


class Stuff(StatesGroup):
    telegram_id = State()
    name = State()
    surname = State()
    username = State()
    role = State()
    phone = State()
