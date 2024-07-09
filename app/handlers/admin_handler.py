from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram import Router, F

from app.lexicon.lexicon_ru import LEXICON_RU, LEXICON_CALLBACK
from app.filtres.custom_filters import isAdmin
from app.state.state_model import Employ, Stuff
from app.models.models import Employee, User
from app.models.roles_enum import RoleEnum
import app.keyboards.keyboards as kb
import app.database.requests as request

router = Router()


router.message.filter(isAdmin())
router.callback_query.filter(isAdmin())


# Назначение нового сотрудника
# State group
@router.callback_query(F.data.startswith(LEXICON_CALLBACK['users_list']))
async def cmd_set_employee(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['choice_user'], reply_markup=await kb.set_employee())


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['set_employee']))
async def cmd_changing_user(callback: CallbackQuery, state: FSMContext):
    telegram_id = int(callback.data.split('_')[1])
    user: User = await request.get_user_by_id(telegram_id=telegram_id)
    await state.set_state(Employ.telegram_id)
    await state.update_data(telegram_id=telegram_id)
    await state.set_state(Employ.username)
    await state.update_data(username=user.username)
    await state.set_state(Employ.name)
    await callback.message.edit_text(text=LEXICON_RU['input_name'])


@router.message(Employ.name)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Employ.surname)
    await message.answer(text=LEXICON_RU['input_surname'])


@router.message(Employ.surname)
async def cmd_set_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Employ.phone)
    await message.answer(text=LEXICON_RU['input_phone_number'])


@router.message(Employ.phone)
async def cmd_set_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    dt = await state.get_data()
    await message.answer(text=f'{LEXICON_RU['employee_name']} {dt["name"]} {dt["surname"]}\n'
                              f'{LEXICON_RU['role']} {RoleEnum.SELLER.value}\n'
                              f'{LEXICON_RU['phone_number']} {dt["phone"]}')
    await request.set_employee(telegram_id=dt["telegram_id"], username=dt["username"],
                               name=dt["name"], surname=dt["surname"], phone=dt["phone"])
    await request.delete_user(telegram_id=dt["telegram_id"])
    await message.answer(text=LEXICON_RU['success'])
    await state.clear()


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['update_employee']))
async def change_stuff(callback: CallbackQuery, state: FSMContext):
    telegram_id = int(callback.data.split('_')[1])
    user_dt: Employee = await request.get_employee_by_id(telegram_id=telegram_id)
    await state.set_state(Stuff.telegram_id)
    await state.update_data(telegram_id=telegram_id)
    await state.set_state(Stuff.username)
    await state.update_data(username=user_dt.username)
    await state.set_state(Stuff.role)
    await state.update_data(role=user_dt.role)
    await state.set_state(Stuff.name)
    await callback.message.edit_text(text=LEXICON_RU['input_name'])


@router.message(Stuff.name)
async def update_employee_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Stuff.surname)
    await message.answer(text=LEXICON_RU['input_surname'])


@router.message(Stuff.surname)
async def update_employee_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Stuff.phone)
    await message.answer(text=LEXICON_RU['input_phone_number'])


@router.message(Stuff.phone)
async def update_employee_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    dt = await state.get_data()
    await message.answer(text=f'{LEXICON_RU['employee_name']} {dt["name"]} {dt["surname"]}\n'
                              f'{LEXICON_RU['role']} {dt["role"]}\n'
                              f'{LEXICON_RU['phone_number']} {dt["phone"]}')
    await request.update_employee(telegram_id=dt["telegram_id"], name=dt["name"], surname=dt["surname"],
                                  phone=dt["phone"], role=dt["role"])
    await message.answer(text=LEXICON_RU['success'])
    await state.clear()


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['role']))
async def cmd_set_role(callback: CallbackQuery):
    telegram_id = int(callback.data.split('_')[1])
    role = str(callback.data.split('_')[2])
    await request.set_role(telegram_id=telegram_id, role=role)
    await callback.answer(text=LEXICON_RU['success'])


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['delete_employee']))
async def cmd_delete_employee(callback: CallbackQuery):
    telegram_id = int(callback.data.split('_')[1])
    await request.delete_employee(telegram_id=telegram_id)
    await callback.answer(text=LEXICON_RU['success'])


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['user']))
async def user(callback: CallbackQuery):
    telegram_id = int(callback.data.split('_')[1])
    user_dt: User = await request.get_user_by_id(telegram_id)
    await callback.message.edit_text(text=f'{LEXICON_RU['username']} {user_dt.username}\n'
                                          f'{LEXICON_RU['tg_id']} {user_dt.telegram_id}')


@router.callback_query(F.data == LEXICON_CALLBACK['guests'])
async def cmd_all_guests(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['choice_user'], reply_markup=await kb.guests_list())
