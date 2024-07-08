from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


import app.keyboards.keyboards as kb
import app.database.requests as request

from app.lexicon.lexicon_ru import LEXICON_RU, LEXICON_CALLBACK
from app.filtres.custom_filters import isStuff
from app.models.models import Employee

router = Router()
# router.message(isStuff())


@router.message(F.text.lower() == 'главная', isStuff())
async def cmd_main(message: Message):
    await message.answer(text=LEXICON_RU['setting'], reply_markup=await kb.cmd_menu(message.from_user.id))


@router.message(F.text.lower() == "каталог", isStuff())
async def cmd_catalog(message: Message):
    await message.answer(text=LEXICON_RU['catalog'], reply_markup=await kb.categories())


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['employee']), isStuff())
async def account(callback: CallbackQuery):
    user_dt: Employee = await request.get_employee_by_id(int(callback.data.split('_')[1]))
    await callback.message.edit_text(text=f'{LEXICON_RU['employee_name']} {user_dt.surname} {user_dt.name}\n'
                                          f'{LEXICON_RU['role']} {user_dt.role}\n'
                                          f'{LEXICON_RU['phone_number']} {user_dt.phone}')
    if await request.is_admin(callback.from_user.id):
        await callback.message.answer(text=LEXICON_RU['update_role'],
                                      reply_markup=await kb.set_role(user_dt.telegram_id))


@router.callback_query(F.data == LEXICON_CALLBACK['employees_list'], isStuff())
async def cmd_employees(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['choice_user'], reply_markup=await kb.employees())


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['product']), isStuff())
async def product_low_access(callback: CallbackQuery):
    product_data = await request.get_product_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(text=f'{LEXICON_RU['product_name']}{product_data.name}\n'
                                       f'{LEXICON_RU['category']}{product_data.category}\n'
                                       f'{LEXICON_RU['balance']}{product_data.balance}\n'
                                       f'{LEXICON_RU['purchase_price']}{int(product_data.cash_price):,}\n'
                                       f'{LEXICON_RU['cash_price']}{int(product_data.credit_price):,}'
                                  .replace(',', ' '),
                                  reply_markup=kb.main)


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['category']), isStuff())
async def category(callback: CallbackQuery):
    category_data = await request.get_category_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(text=f'{LEXICON_RU['category_list']}<b>{category_data.name}</b>:',
                                  reply_markup=await kb.product(category_data.name))


@router.message(isStuff())
async def cmd_search(message: Message):
    await message.answer(text=LEXICON_RU['search_reply'], reply_markup=await kb.search_product(message.text.lower()))
