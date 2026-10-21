from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MedForm
from core.ocr import extract_text_from_image, analyze_image_color
from core.facts_db import check_fact
from keyboards.main_menu import after_answer_kb

router = Router()

MEDICINE_KEYWORDS = ["таблетки", "капсулы", "мг", "мл", "раствор", "мазь", "гель", "дозировка", "инструкция", "противопоказания", "активное вещество"]

@router.message(MedForm.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    await message.answer("⏳ Анализирую фотографию...")
    
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file = await message.bot.download_file(file_info.file_path)
    image_bytes = file.read()
    
    text = extract_text_from_image(image_bytes)
    
    if text and len(text) > 20:
        text_lower = text.lower()
        is_medicine = any(kw in text_lower for kw in MEDICINE_KEYWORDS)
        
        if is_medicine:
            result = check_fact(text)
            if result:
                response = f"💊 <b>Похоже на лекарство. Распознанный текст:</b>\n<i>{text[:200]}...</i>\n\n"
                response += f"✅ <b>Найдено в базе:</b> {result['verdict']}\n{result['explanation']}"
            else:
                response = (
                    f"💊 <b>Это лекарство.</b>\n\n"
                    f"📸 <b>Распознанный текст:</b>\n<i>{text[:300]}...</i>\n\n"
                    f"⚠️ <i>Я не могу проверить качество этого лекарства. Обязательно проверьте инструкцию и срок годности. "
                    f"Не принимайте препараты без назначения врача!</i>"
                )
        else:
            result = check_fact(text)
            if result:
                response = f"📸 <b>Распознанный текст:</b>\n<i>{text[:200]}...</i>\n\n{result['verdict']}\n{result['explanation']}"
            else:
                response = f"📸 <b>Распознанный текст:</b>\n<i>{text[:500]}...</i>\n\n🤔 Я не нашел здесь известных болезней."
    else:
        color_type = analyze_image_color(image_bytes)
        
        if color_type == "red_dominant":
            response = (
                "🔴 <b>На фото преобладает красный цвет.</b>\n\n"
                "Похоже на сыпь, покраснение или рану. <b>Я не могу поставить диагноз по фотографии</b> — "
                "это опасно. Пожалуйста, опишите симптомы словами (где болит, как давно) или обратитесь к врачу (дерматологу/хирургу)."
            )
        else:
            response = (
                "❓ <b>Я не вижу текста на фото.</b>\n\n"
                "Если это перелом, травма или кожное заболевание — я не могу распознать это по картинке. "
                "Пожалуйста, опишите, что случилось, словами, или обратитесь к врачу."
            )
        
    await message.answer(response, parse_mode="HTML", reply_markup=after_answer_kb())
    await state.clear()

@router.message(F.photo)
async def handle_unexpected_photo(message: Message):
    await message.answer(
        "📸 Нажмите кнопку <b>«📸 Проверить фото»</b> в меню, чтобы я понял, что вы хотите проверить.",
        parse_mode="HTML",
        reply_markup=after_answer_kb()
    )