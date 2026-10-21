from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import MedForm

router = Router()


@router.message(MedForm.age)
async def process_age(message: Message, state: FSMContext):
    age_text = message.text.strip()
    if not age_text.isdigit() or not (0 < int(age_text) < 120):
        await message.answer("Пожалуйста, введите корректный возраст (число от 1 до 119).")
        return
    await state.update_data(age=int(age_text))
    await message.answer("Ваш пол? Напишите «М» или «Ж».")
    await state.set_state(MedForm.gender)


@router.message(MedForm.gender)
async def process_gender(message: Message, state: FSMContext):
    gender = message.text.strip().lower()
    if gender not in ["м", "ж", "муж", "жен", "мужской", "женский"]:
        await message.answer("Пожалуйста, введите «М» или «Ж».")
        return
    await state.update_data(gender=gender[0].upper())
    await message.answer("Ваш вес в кг? (например, 70)")
    await state.set_state(MedForm.weight)


@router.message(MedForm.weight)
async def process_weight(message: Message, state: FSMContext):
    weight_text = message.text.strip().replace(",", ".")
    try:
        weight = float(weight_text)
        if not (2 < weight < 400):
            raise ValueError
    except ValueError:
        await message.answer("Введите корректный вес (например, 70).")
        return
    await state.update_data(weight=weight)
    await message.answer(
        "📝 Теперь опишите ваши симптомы.\n\n"
        "Например: «Температура 38, насморк, болит горло»."
    )
    await state.set_state(MedForm.symptoms)