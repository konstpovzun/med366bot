from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import DISCLAIMER, CONSENT_TEXT
from states import MedForm
from keyboards.main_menu import consent_kb, after_answer_kb, start_menu_kb
from core.db import get_user_profile

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(DISCLAIMER, parse_mode="HTML")
    await message.answer(
        "🤖 <b>Чем я могу помочь?</b>\n\n"
        "Выберите один из вариантов ниже:\n\n"
        "🩺 <b>Описать симптомы</b> — напишите, что вас беспокоит. Я подскажу базовые шаги и врача.\n\n"
        "🔗 <b>Проверить ссылку</b> — пришлите ссылку, и я проверю, заслуживает ли источник доверия.\n\n"
        "🔍 <b>Проверить факт</b> — напишите миф (например, «антибиотики лечат вирусы»). Я скажу, правда это или нет.\n\n"
        "📸 <b>Проверить фото</b> — пришлите фото справки, анализа или упаковки лекарства. Я распознаю текст и проверю его.\n\n"
        "🎥 <b>Проверить видео</b> — запишите видео с описанием симптомов, я распознаю речь.",
        parse_mode="HTML",
        reply_markup=start_menu_kb()
    )
    await state.set_state(MedForm.choose_action)


@router.callback_query(F.data == "action_symptoms", MedForm.choose_action)
async def action_symptoms(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    profile = get_user_profile(user_id)

    if profile:
        await callback.message.edit_text(
            f"С возвращением! Я помню ваши данные: возраст {profile['age']}, "
            f"пол {profile['gender']}, вес {profile['weight']} кг.\n\n"
            "📝 Опишите ваши симптомы:",
            parse_mode="HTML"
        )
        await state.update_data(**profile)
        await state.set_state(MedForm.symptoms)
    else:
        await callback.message.edit_text(CONSENT_TEXT, parse_mode="HTML", reply_markup=consent_kb())
        await state.set_state(MedForm.consent)
    await callback.answer()


@router.callback_query(F.data == "action_link", MedForm.choose_action)
async def action_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте мне ссылку на статью или сайт, и я проверю источник.")
    await state.set_state(MedForm.link)
    await callback.answer()


@router.callback_query(F.data == "action_fact", MedForm.choose_action)
async def action_fact(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напишите медицинский факт или утверждение, которое хотите проверить.\n\n"
        "Например: «рак передается воздушно-капельным путем»"
    )
    await state.set_state(MedForm.fact)
    await callback.answer()


@router.callback_query(F.data == "action_photo", MedForm.choose_action)
async def action_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📸 Отправьте мне фотографию справки, анализа или упаковки лекарства.\n\n"
        "Я постараюсь распознать текст и проверить его. "
        "⚠️ <i>Если на фото кожное заболевание (сыпь), я не смогу его распознать — опишите симптомы словами.</i>",
        parse_mode="HTML"
    )
    await state.set_state(MedForm.photo)
    await callback.answer()


@router.callback_query(F.data == "action_video", MedForm.choose_action)
async def action_video(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎥 Отправьте мне видео с описанием симптомов или медицинского факта. "
        "Я распознаю речь и проверю текст.\n\n"
        "⚠️ <i>Длина видео не должна превышать 1-2 минуты для быстрой обработки.</i>",
        parse_mode="HTML"
    )
    await state.set_state(MedForm.video)
    await callback.answer()


@router.callback_query(F.data == "consent_yes", MedForm.consent)
async def consent_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✅ Спасибо! Согласие получено.")
    await callback.message.answer("Сколько вам лет?")
    await state.set_state(MedForm.age)
    await callback.answer()


@router.callback_query(F.data == "consent_no", MedForm.consent)
async def consent_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "❌ Без согласия я не могу продолжить.\n\n"
        "Если передумаете — нажмите /start."
    )
    await state.clear()
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🤖 <b>Как я работаю:</b>\n\n"
        "1. Вы выбираете: описать симптомы, проверить ссылку, факт, фото или видео.\n"
        "2. Если симптомы — я спрашиваю возраст, пол, вес.\n"
        "3. Проверяю на «красные флаги».\n"
        "4. Даю рекомендацию.\n\n"
        "<b>Команды:</b>\n"
        "/start — начать\n"
        "/help — эта справка",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "new_request")
async def new_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🤖 <b>Чем я могу помочь?</b>\n\n"
        "Выберите один из вариантов ниже:\n\n"
        "🩺 <b>Описать симптомы</b> — напишите, что вас беспокоит.\n"
        "🔗 <b>Проверить ссылку</b> — пришлите ссылку на статью.\n"
        "🔍 <b>Проверить факт</b> — напишите миф.\n"
        "📸 <b>Проверить фото</b> — пришлите фото справки или лекарства.\n"
        "🎥 <b>Проверить видео</b> — запишите видео с описанием.",
        parse_mode="HTML",
        reply_markup=start_menu_kb()
    )
    await state.set_state(MedForm.choose_action)
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🤖 <b>Я помогаю с симптомами, проверяю ссылки, факты, фото и видео.</b>\n\n"
        "Нажмите /start, чтобы начать заново.",
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "check_link")
async def check_link_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте мне ссылку на статью или сайт, и я проверю источник.")
    await state.set_state(MedForm.link)
    await callback.answer()


@router.callback_query(F.data == "check_fact")
async def check_fact_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Напишите медицинский факт или утверждение, которое хотите проверить.\n\n"
        "Например: «рак передается воздушно-капельным путем»"
    )
    await state.set_state(MedForm.fact)
    await callback.answer()


@router.callback_query(F.data == "check_photo")
async def check_photo_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📸 Отправьте мне фотографию справки, анализа или упаковки лекарства.\n\n"
        "⚠️ <i>Если на фото кожное заболевание (сыпь), я не смогу его распознать — опишите симптомы словами.</i>",
        parse_mode="HTML"
    )
    await state.set_state(MedForm.photo)
    await callback.answer()

@router.callback_query(F.data == "check_video")
async def check_video_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🎥 Отправьте мне видео с описанием симптомов или медицинского факта. "
        "Я распознаю речь и проверю текст.\n\n"
        "⚠️ <i>Длина видео не должна превышать 1-2 минуты для быстрой обработки.</i>",
        parse_mode="HTML"
    )
    await state.set_state(MedForm.video)
    await callback.answer()