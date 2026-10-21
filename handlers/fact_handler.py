from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MedForm
from core.facts_db import check_fact, search_who
from keyboards.main_menu import after_answer_kb

router = Router()

@router.message(MedForm.fact)
async def process_fact(message: Message, state: FSMContext):
    claim = message.text.strip()
    
    data = await state.get_data()
    last_topic = data.get("last_topic", None)
    
    result = check_fact(claim, last_topic)
    
    if result:
        if result.get("topic"):
            await state.update_data(last_topic=result["topic"])
            
        # Формируем ответ с блоком "Что делать"
        response = f"{result['verdict']}\n\n📝 {result['explanation']}\n\n"
        
        if result.get("actions"):
            response += f"💊 <b>Действия:</b>\n{result['actions']}\n\n"
            
        response += f"📚 <b>Источник:</b> <a href='{result['url']}'>{result['source']}</a>"
    else:
        await message.answer("⏳ Анализируем информацию в медицинских базах...")
        medical_result = search_who(claim)
        
        if medical_result:
            await state.update_data(last_topic=claim)
            response = (
                f"🤔 <b>Нашел информацию:</b>\n\n"
                f"📖 <a href='{medical_result['url']}'>{medical_result['title']}</a>\n\n"
                f"📚 <b>Источник:</b> {medical_result['source']}"
            )
        else:
            response = (
                "🤔 <b>Я не нашел этот факт.</b>\n\n"
                "Попробуйте переформулировать утверждение или отправьте ссылку на статью."
            )
    
    await message.answer(response, parse_mode="HTML", reply_markup=after_answer_kb())
    await state.set_state(MedForm.fact)