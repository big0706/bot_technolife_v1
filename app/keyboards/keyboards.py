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
def set_role(telegram_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=RoleEnum.ADMIN.value,
                                                                callback_data=f'{LEXICON_CALLBACK['role']}'
                                                                              f'{telegram_id}_{RoleEnum.ADMIN.value}'),
                                           InlineKeyboardButton(text=RoleEnum.MANAGER.value,
                                                                callback_data=f'{LEXICON_CALLBACK['role']}'
                                                                              f'{telegram_id}_'
                                                                              f'{RoleEnum.MANAGER.value}'),
                                           InlineKeyboardButton(text=RoleEnum.SELLER.value,
                                                                callback_data=f'{LEXICON_CALLBACK['role']}'
                                                                              f'{telegram_id}_{RoleEnum.SELLER.value}'),
                                           ]
    keyboard.row(*buttons,width=3)
    keyboard.row(InlineKeyboardButton(text=LEXICON_BUTTON['change_dt'],
                                      callback_data=f'{LEXICON_CALLBACK['update_employee']}{telegram_id}'))

    keyboard.row(InlineKeyboardButton(text=LEXICON_BUTTON['delete_employee'],
                                      callback_data=f'{LEXICON_CALLBACK['delete_employee']}{telegram_id}'))

    return keyboard.as_markup()


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
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=LEXICON_BUTTON['account'],
                                                                callback_data=f'{LEXICON_CALLBACK['employee']}'
                                                                              f'{telegram_id}'),
                                           InlineKeyboardButton(text=LEXICON_BUTTON['employee_list'],
                                                                callback_data=LEXICON_CALLBACK['employees_list'])]
    if await is_admin(telegram_id):
        buttons.append(InlineKeyboardButton(text=LEXICON_BUTTON['set_employee'],
                                            callback_data=LEXICON_CALLBACK['users_list']))
        buttons.append(InlineKeyboardButton(text=LEXICON_BUTTON['guests_list'],
                                            callback_data=LEXICON_CALLBACK['guests']))
    keyboard.row(*buttons, width=2)
    return keyboard.as_markup()


# Список категорий
async def categories() -> InlineKeyboardMarkup:
    all_categories: list[Category] = await get_categories()
    buttons: list[InlineKeyboardButton] = []
    keyboard = InlineKeyboardBuilder()
    for c in all_categories:
        buttons.append(InlineKeyboardButton(text=c.name, callback_data=f'{LEXICON_CALLBACK['category']}{c.id}'))
    keyboard.row(*buttons, width=2)
    return keyboard.as_markup()


# Список товаров
async def product(category_name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_category(category_name)
    buttons: list[InlineKeyboardButton] = []
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        buttons.append(InlineKeyboardButton(text=p.name, callback_data=f'{LEXICON_CALLBACK['product']}{p.id}'))
    keyboard.row(*buttons)
    return keyboard.adjust(1).as_markup()


# Список найденных товаров
async def search_product(name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_search(name)
    buttons: list[InlineKeyboardButton] = []
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        keyboard.add(InlineKeyboardButton(text=p.name, callback_data=f'{LEXICON_CALLBACK['product']}{p.id}'))
    keyboard.row(*buttons)
    return keyboard.adjust(1).as_markup()
