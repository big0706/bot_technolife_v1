from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router

from app.lexicon.lexicon_ru import LEXICON_RU
import app.keyboards.keyboards as kb
import app.database.requests as request


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if await request.is_guest(message.from_user.id):
        await request.set_user(telegram_id=message.from_user.id, username=message.from_user.username)
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=kb.main)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=kb.main)
