from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import *
from app.models.models import User
from app.lexicon.lexicon_ru import LEXICON_BUTTON, LEXICON_CALLBACK

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=LEXICON_BUTTON['main']),
                                     KeyboardButton(text=LEXICON_BUTTON['catalog'])]],
                           resize_keyboard=True,
                           one_time_keyboard=True,
                           input_field_placeholder=LEXICON_BUTTON['example'])


# Смена роли и данных сотрудника
async def set_role(telegram_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=RoleEnum.ADMIN.value,
                                      callback_data=f'{LEXICON_CALLBACK['role']}{telegram_id}_'
                                                    f'{RoleEnum.ADMIN.value}'))
    keyboard.add(InlineKeyboardButton(text=RoleEnum.MANAGER.value,
                                      callback_data=f'{LEXICON_CALLBACK['role']}{telegram_id}_'
                                                    f'{RoleEnum.MANAGER.value}'))
    keyboard.add(InlineKeyboardButton(text=RoleEnum.SELLER.value,
                                      callback_data=f'{LEXICON_CALLBACK['role']}{telegram_id}_'
                                                    f'{RoleEnum.SELLER.value}'))
    keyboard.add(InlineKeyboardButton(text=LEXICON_BUTTON['change_dt'],
                                      callback_data=f'{LEXICON_CALLBACK['update_employee']}{telegram_id}'))
    return keyboard.adjust(2).as_markup()


# Назначение пользователя в сотрудника
async def set_employee() -> InlineKeyboardMarkup:
    all_users: list[User] = await get_users()
    keyboard = InlineKeyboardBuilder()
    for u in all_users:
        keyboard.add(InlineKeyboardButton(text=f'{u.username}', callback_data=f'{LEXICON_CALLBACK['set_employee']}'
                                                                              f'{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()


# Список сотрудников
async def employees() -> InlineKeyboardMarkup:
    all_employs: list[Employee] = await get_employees()
    keyboard = InlineKeyboardBuilder()
    for u in all_employs:
        keyboard.add(InlineKeyboardButton(text=f'{u.surname} {u.name}', callback_data=f'{LEXICON_CALLBACK['employee']}'
                                                                                      f'{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()


# Список незарегистрированных пользователей
async def guests_list() -> InlineKeyboardMarkup:
    all_users: list[User] = await get_users()
    keyboard = InlineKeyboardBuilder()
    for u in all_users:
        keyboard.add(InlineKeyboardButton(text=f'{u.username}',
                                          callback_data=f'{LEXICON_CALLBACK['user']}{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()


# Главная
async def cmd_menu(telegram_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=LEXICON_BUTTON['account'],
                                      callback_data=f'{LEXICON_CALLBACK['employee']}{telegram_id}'))
    keyboard.add(InlineKeyboardButton(text=LEXICON_BUTTON['employee_list'],
                                      callback_data=LEXICON_CALLBACK['employees_list']))
    if await is_admin(telegram_id):
        keyboard.add(InlineKeyboardButton(text=LEXICON_BUTTON['set_employee'],
                                          callback_data=LEXICON_CALLBACK['users_list']))
        keyboard.add(InlineKeyboardButton(text=LEXICON_BUTTON['guests_list'],
                                          callback_data=LEXICON_CALLBACK['guests']))
    return keyboard.adjust(1).as_markup()


# Список категорий
async def categories() -> InlineKeyboardMarkup:
    all_categories: list[Category] = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for c in all_categories:
        keyboard.add(InlineKeyboardButton(text=c.name, callback_data=f'{LEXICON_CALLBACK['category']}{c.id}'))
    return keyboard.adjust(2).as_markup()


# Список товаров
async def product(category_name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_category(category_name)
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        keyboard.add(InlineKeyboardButton(text=p.name, callback_data=f'{LEXICON_CALLBACK['product']}{p.id}'))
    return keyboard.adjust(1).as_markup()


# Список найденных товаров
async def search_product(name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_search(name)
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        keyboard.add(InlineKeyboardButton(text=p.name, callback_data=f'{LEXICON_CALLBACK['product']}{p.id}'))
    return keyboard.adjust(1).as_markup()
