from aiogram import Router
from aiogram.types import Message

from app.lexicon.lexicon_ru import LEXICON_RU

router = Router()


@router.message()
async def not_users(message: Message):
    await message.answer(text=LEXICON_RU['not_access'])
