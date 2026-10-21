from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def fallback(message: Message):
    await message.answer(
        "🤖 Я понимаю только текстовые описания симптомов.\n\n"
        "Нажмите /start чтобы начать, или /help для справки."
    )