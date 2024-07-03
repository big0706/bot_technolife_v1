from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import *


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Главная')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбери пункт меню или напиши наименование '
                                                   'товара для поиска')


async def set_role(telegram_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=Role.ADMIN.value,
                                      callback_data=f'role_{telegram_id}_{Role.ADMIN.value}'))
    keyboard.add(InlineKeyboardButton(text=Role.MANAGER.value,
                                      callback_data=f'role_{telegram_id}_{Role.MANAGER.value}'))
    keyboard.add(InlineKeyboardButton(text=Role.SELLER.value,
                                      callback_data=f'role_{telegram_id}_{Role.SELLER.value}'))
    keyboard.add(InlineKeyboardButton(text=Role.GUEST.value,
                                      callback_data=f'role_{telegram_id}_{Role.GUEST.value}'))
    keyboard.add(InlineKeyboardButton(text='Изменить данные сотрудника',
                                      callback_data=f'set_{telegram_id}'))
    return keyboard.adjust(2).as_markup()


async def cmd_menu(telegram_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Моя анкета', callback_data=f'user_{telegram_id}'))
    if await is_admin(telegram_id):
        keyboard.add(InlineKeyboardButton(text='Список сотрудников', callback_data='employs'))
        keyboard.add(InlineKeyboardButton(text='Назначить сотрудника', callback_data='set_member'))
        keyboard.add(InlineKeyboardButton(text='Все гости', callback_data='all_users'))
    if await is_manager(telegram_id):
        keyboard.add(InlineKeyboardButton(text='Список сотрудников', callback_data='employs'))
    return keyboard.adjust(1).as_markup()


async def categories() -> InlineKeyboardMarkup:
    all_categories: list[Category] = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for c in all_categories:
        keyboard.add(InlineKeyboardButton(text=c.name, callback_data=f'category_{c.id}'))
    return keyboard.adjust(2).as_markup()


async def product(category_name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_category(category_name)
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        keyboard.add(InlineKeyboardButton(text=p.name, callback_data=f'product_{p.id}'))
    return keyboard.adjust(1).as_markup()


async def search_product(name: str) -> InlineKeyboardMarkup:
    all_products: list[Product] = await get_products_by_search(name)
    keyboard = InlineKeyboardBuilder()
    for p in all_products:
        keyboard.add(InlineKeyboardButton(text=p.name, callback_data=f'product_{p.id}'))
    return keyboard.adjust(1).as_markup()


async def employs() -> InlineKeyboardMarkup:
    all_employs: list[User] = await get_employs()
    keyboard = InlineKeyboardBuilder()
    for u in all_employs:
        keyboard.add(InlineKeyboardButton(text=f'{u.last_name} {u.first_name}', callback_data=f'user_{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()


async def set_member() -> InlineKeyboardMarkup:
    all_users: list[User] = await get_users()
    keyboard = InlineKeyboardBuilder()
    for u in all_users:
        keyboard.add(InlineKeyboardButton(text=f'{u.username}', callback_data=f'set_{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()


async def list_guests() -> InlineKeyboardMarkup:
    all_users: list[User] = await get_users()
    keyboard = InlineKeyboardBuilder()
    for u in all_users:
        keyboard.add(InlineKeyboardButton(text=f'{u.username} {u.role}',
                                          callback_data=f'user_{u.telegram_id}'))
    return keyboard.adjust(1).as_markup()
