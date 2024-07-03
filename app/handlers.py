from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as request

from app.filtres import custom_filters as filters
from app.state import Employ
from app.database.models import User, Role


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    if await request.is_guest(message.from_user.id):
        await request.set_user(message.from_user.id, message.from_user.username)
    await message.answer('Хей! Сейчас проверю, есть ли у тебя доступ.\n'
                         'Жми на каталог',
                         reply_markup=kb.main)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer('Всё очень просто, если ты сотрудник, то есть доступ.\n'
                         'Жми на каталог или пиши в сообщениях модель, для поиска.',
                         reply_markup=kb.main)


@router.message(F.text.lower() == 'главная', filters.isStuff())
async def main(message: Message):
    await message.answer(f'Доступные опции:', reply_markup=await kb.cmd_menu(message.from_user.id))


@router.message(F.text.lower() == "каталог", filters.isStuff())
async def catalog(message: Message):
    await message.answer('Выбери категорию товара:', reply_markup=await kb.categories())


# Назначение сотрудника из списка пользователей
@router.callback_query(F.data.startswith("set_member"), filters.isAdmin())
async def set_member(callback: CallbackQuery):
    await callback.message.answer('Выберите пользователя из списка:', reply_markup=await kb.set_member())


@router.callback_query(F.data.startswith("set_"), filters.isAdmin())
async def set_employ(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Employ.telegram_id)
    await state.update_data(telegram_id=int(callback.data.split('_')[1]))
    await state.set_state(Employ.first_name)
    await callback.message.answer('Введите имя сотрудника')


@router.message(Employ.first_name, filters.isAdmin())
async def set_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Employ.last_name)
    await message.answer('Введите фамилию сотрудника')


@router.message(Employ.last_name, filters.isAdmin())
async def set_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Employ.phone)
    await message.answer('Введите номер телефона в таком формате +7 777 777 7777')


@router.message(Employ.phone, filters.isAdmin())
async def set_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    dt = await state.get_data()
    await message.answer(f'Пользователь: {dt["first_name"]} {dt["last_name"]}\n'
                         f'Статус: {Role.SELLER.value}\n'
                         f'Телефон номер: {dt["phone"]}')
    await request.set_employ(dt["telegram_id"], dt["first_name"], dt["last_name"], dt["phone"])
    await message.answer('Сотрудник успешно добавлен')
    await state.clear()


# Анкета пользоваля по id, с дополнительным функционалом для роли: admin
@router.callback_query(F.data.startswith("user_"), filters.isStuff())
async def user(callback: CallbackQuery):
    user_dt: User = await request.get_user_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(f'Пользователь: {user_dt.last_name} {user_dt.first_name}\n'
                                  f'Никнейм телеграмма: {user_dt.username}\n'
                                  f'Статус: {user_dt.role}\n'
                                  f'Телефон номер: {user_dt.phone}')
    if await request.is_admin(callback.from_user.id):
        await callback.message.answer('Сменить роль:', reply_markup=await kb.set_role(user_dt.telegram_id))


# Смена роли пользователя
@router.callback_query(F.data.startswith("role_"), filters.isAdmin())
async def set_role(callback: CallbackQuery):
    await request.set_role(int(callback.data.split('_')[1]), str(callback.data.split('_')[2]))
    await callback.message.answer('Успешно')


# Список зарегистрированных сотрудников
@router.callback_query(F.data == "employs", filters.isAdmin() or filters.isManager())
async def employ(callback: CallbackQuery):
    await callback.message.answer('Список сотрудников:', reply_markup=await kb.employs())


# Список не зарегистрированных пользователей
@router.callback_query(F.data == "all_users", filters.isAdmin() or filters.isManager())
async def all_users(callback: CallbackQuery):
    await callback.message.answer('Все гости:', reply_markup=await kb.list_guests())


# Список категорий
@router.callback_query(F.data.startswith("category_"), filters.isStuff())
async def category(callback: CallbackQuery):
    category_data = await request.get_category_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(f'Список товаров в категории {category_data.name}:',
                                  reply_markup=await kb.product(category_data.name))


# Отображение товара с дополнительным полем, для роли: admin, manager
@router.callback_query(F.data.startswith("product_"), filters.isAdmin() or filters.isManager())
async def product_high_access(callback: CallbackQuery):
    product_data = await request.get_product_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(f'Наименование: {product_data.name}\n'
                                  f'Категория: {product_data.category}\n'
                                  f'Остаток: {product_data.balance}\n'
                                  f'Закупочная: {int(product_data.purchase_price):,}\n'
                                  f'Наличными: {int(product_data.cash_price):,}\n'
                                  f'Кредит: {int(product_data.credit_price):,}'.replace(',', ' '),
                                  reply_markup=kb.main)


# Отображение товара ля всех ролей
@router.callback_query(F.data.startswith("product_"), filters.isStuff())
async def product_low_access(callback: CallbackQuery):
    product_data = await request.get_product_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(f'Наименование: {product_data.name}\n'
                                  f'Категория: {product_data.category}\n'
                                  f'Остаток: {product_data.balance}\n'
                                  f'Наличными: {int(product_data.cash_price):,}\n'
                                  f'Кредит: {int(product_data.credit_price):,}'.replace(',', ' '),
                                  reply_markup=kb.main)


# Поиск по названию
@router.message(filters.isStuff())
async def search(message: Message):
    await message.answer('Вот что удалось найти:', reply_markup=await kb.search_product(message.text.lower()))


# Вывод сообщения для незарегистрированных пользователей
@router.message()
async def not_users(message: Message):
    await message.answer('Ой, а ты то не в списке сотрудников. Пиши админу.')
