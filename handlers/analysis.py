from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import MedForm
from core.red_flags import check_red_flags, get_symptom_advice
from keyboards.main_menu import after_answer_kb

router = Router()

@router.message(MedForm.symptoms)
@router.message(MedForm.symptoms_clarify)
async def process_symptoms(message: Message, state: FSMContext):
    data = await state.get_data()
    # Защита от None
    age = data.get('age', 'Не указан')
    gender = data.get('gender', 'Не указан')
    weight = data.get('weight', 'Не указан')
    
    symptoms = message.text.strip()

    if len(symptoms) < 15:
        await message.answer(
            "🤔 Пожалуйста, опишите подробнее.\n\n"
            "Что именно болит? Где болит? Как давно? Есть ли температура или другие симптомы?\n\n"
            "Например: <i>«Болит голова в висках уже два дня, температура 37.5»</i>.",
            parse_mode="HTML"
        )
        await state.set_state(MedForm.symptoms_clarify) 
        return

    red = check_red_flags(symptoms, age if isinstance(age, int) else 30)
    
    if "MYALGIA_AFTER_COUGH" in red:
        red.remove("MYALGIA_AFTER_COUGH")
        if not red:
            categories = get_symptom_advice(symptoms)
            response_text = (
                f"📋 <b>Ваши данные:</b>\n"
                f"• Возраст: {age}\n"
                f"• Пол: {gender}\n"
                f"• Вес: {weight} кг\n\n"
                f"🩺 <b>Рекомендации:</b>\n\n"
                f"<b>🔹 Боль в груди при кашле:</b>\n"
                f"  • Это мышечная боль от сильного кашля (миалгия).\n"
                f"  • Старайтесь не перенапрягать мышцы, при кашле придерживайте грудь.\n"
                f"  • Примите безрецептурное обезболивающее (парацетамол/ибупрофен).\n"
                f"  • Если боль станет давящей или появится одышка — срочно к врачу!\n\n"
            )
            if categories:
                for cat_name, cat_data in categories.items():
                    response_text += f"<b>🔹 {cat_name}:</b>\n"
                    for advice in cat_data["advice"]:
                        response_text += f"  • {advice}\n"
                    response_text += "\n"
            response_text += (
                f"👨‍⚕️ <b>К какому врачу обратиться:</b>\n"
                f"  Терапевт или пульмонолог\n\n"
                "⚠️ <i>Если состояние ухудшится или не улучшится за 3 дня, "
                "я советую вам обратиться за врачебной помощью.</i>"
            )
            await message.answer(response_text, parse_mode="HTML", reply_markup=after_answer_kb())
            await state.clear()
            return

    if red:
        await message.answer(
            "🚨 <b>ВНИМАНИЕ!</b>\n\n"
            f"Обнаружены тревожные симптомы: <b>{', '.join(red)}</b>\n\n"
            "❗ <b>Немедленно обратитесь к врачу или вызовите скорую (103, 112).</b>\n\n"
            "Я не могу давать рекомендации в этой ситуации — это опасно для жизни.",
            parse_mode="HTML",
            reply_markup=after_answer_kb()
        )
        await state.clear()
        return

    categories = get_symptom_advice(symptoms)
    
    if categories:
        response_text = (
            f"📋 <b>Ваши данные:</b>\n"
            f"• Возраст: {age}\n"
            f"• Пол: {gender}\n"
            f"• Вес: {weight} кг\n\n"
            f"🩺 <b>Рекомендации по вашим симптомам:</b>\n\n"
        )
        doctors = set()
        for cat_name, cat_data in categories.items():
            response_text += f"<b>🔹 {cat_name}:</b>\n"
            for advice in cat_data["advice"]:
                response_text += f"  • {advice}\n"
            response_text += "\n"
            doctors.add(cat_data["doctor"])

        response_text += (
            f"👨‍⚕️ <b>К какому врачу обратиться:</b>\n"
            f"  {', '.join(doctors)}\n\n"
            "⚠️ <i>Если состояние ухудшится или не улучшится за 3 дня, "
            "я советую вам обратиться за врачебной помощью.</i>"
        )
        await message.answer(response_text, parse_mode="HTML", reply_markup=after_answer_kb())
    else:
        await message.answer(
            f"📋 <b>Ваши данные:</b>\n"
            f"• Возраст: {age}\n"
            f"• Пол: {gender}\n"
            f"• Вес: {weight} кг\n\n"
            "🤔 Я не могу точно определить ваше состояние по описанию.\n\n"
            "👨‍⚕️ <b>К какому врачу обратиться:</b>\n"
            "  Терапевт (для первичного осмотра)\n\n"
            "⚠️ <i>Я советую вам обратиться за врачебной помощью.</i>",
            parse_mode="HTML",
            reply_markup=after_answer_kb()
        )

    await state.clear()