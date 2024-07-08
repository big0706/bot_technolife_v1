from aiogram import Router, F
from aiogram.types import CallbackQuery

import app.keyboards.keyboards as kb
import app.database.requests as request

from app.filtres.custom_filters import isManager
from app.lexicon.lexicon_ru import LEXICON_RU, LEXICON_CALLBACK

router = Router()


# router.message(isManager())


@router.callback_query(F.data.startswith(LEXICON_CALLBACK['product']), isManager())
async def product_high_access(callback: CallbackQuery):
    product_data = await request.get_product_by_id(int(callback.data.split('_')[1]))
    await callback.message.answer(text=f'{LEXICON_RU['product_name']}{product_data.name}\n'
                                       f'{LEXICON_RU['category']}{product_data.category}\n'
                                       f'{LEXICON_RU['balance']}{product_data.balance}\n'
                                       f'{LEXICON_RU['purchase_price']}{int(product_data.purchase_price):,}\n'
                                       f'{LEXICON_RU['cash_price']}{int(product_data.cash_price):,}\n'
                                       f'{LEXICON_RU['credit_price']}{int(product_data.credit_price):,}'
                                  .replace(',', ' '),
                                  reply_markup=kb.main)
