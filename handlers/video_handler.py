from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MedForm
from core.video_processor import transcribe_video
from core.facts_db import check_fact
from keyboards.main_menu import after_answer_kb
import os
import tempfile

router = Router()

@router.message(MedForm.video, F.video)
async def process_video(message: Message, state: FSMContext):
    await message.answer("⏳ Распознаю речь из видео... Это может занять до 30 секунд.")
    
    video = message.video
    file_info = await message.bot.get_file(video.file_id)
    file = await message.bot.download_file(file_info.file_path)
    
    # Сохраняем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
        
    try:
        text = transcribe_video(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path) # Удаляем временный файл
        
    if not text:
        await message.answer("❌ Не удалось распознать речь. Попробуйте записать видео с более четкой речью.", reply_markup=after_answer_kb())
        await state.clear()
        return
        
    result = check_fact(text)
    
    if result:
        response = (
            f"🎥 <b>Распознанная речь:</b>\n<i>{text[:300]}...</i>\n\n"
            f"{result['verdict']}\n\n"
            f"📝 {result['explanation']}\n\n"
            f"📚 <b>Источник:</b> <a href='{result['url']}'>{result['source']}</a>"
        )
    else:
        response = (
            f"🎥 <b>Распознанная речь:</b>\n<i>{text[:500]}...</i>\n\n"
            f"🤔 Я не нашел в этом тексте известных болезней или мифов.\n\n"
            f"💡 <i>Попробуйте описать симптомы текстом, чтобы получить рекомендации.</i>"
        )
        
    await message.answer(response, parse_mode="HTML", reply_markup=after_answer_kb())
    await state.clear()

@router.message(F.video)
async def handle_unexpected_video(message: Message):
    await message.answer(
        "🎥 Нажмите кнопку <b>«🎥 Проверить видео»</b> в меню, чтобы я понял, что вы хотите проверить.",
        parse_mode="HTML",
        reply_markup=after_answer_kb()
    )