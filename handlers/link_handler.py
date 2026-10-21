from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MedForm
from core.trusted_sources import check_domain
from core.parser import extract_text_from_url, analyze_text_for_myths # Импортируем новую функцию
from keyboards.main_menu import after_answer_kb
from urllib.parse import urlparse

router = Router()

BLACKLIST = ["vk.com", "vk.ru", "ok.ru", "facebook.com", "instagram.com", "t.me", "twitter.com", "x.com", "youtube.com", "tiktok.com", "dzen.ru", "zen.yandex.ru", "pikabu.ru", "reddit.com", "porn", "sex", "xxx", "adult"]

@router.message(MedForm.link)
async def process_link(message: Message, state: FSMContext):
    url = message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.answer("❌ <b>Неверный формат ссылки.</b>\n\nПожалуйста, отправьте полную ссылку (начиная с http://).", parse_mode="HTML")
        return

    domain = urlparse(url).netloc.replace("www.", "")
    if any(social in domain for social in BLACKLIST):
        await message.answer("🚫 <b>Это не медицинский источник.</b>\n\nЯ не анализирую соцсети и видео.", parse_mode="HTML", reply_markup=after_answer_kb())
        await state.clear()
        return

    await message.answer("⏳ Анализируем источник...")
    
    domain_info = check_domain(url)
    text = extract_text_from_url(url)
    
    if not text:
        await message.answer("❌ <b>Не удалось прочитать текст статьи.</b>\n\nВозможно, сайт блокирует парсинг.", parse_mode="HTML", reply_markup=after_answer_kb())
        await state.clear()
        return

    # Проверяем текст на мифы
    myth_warning = analyze_text_for_myths(text)
    
    # Формируем вердикт
    if domain_info["trusted"]:
        verdict = "✅ <b>ДОСТОВЕРНЫЙ ИСТОЧНИК</b>"
        reason = f"Домен входит в белый список ({domain_info['name']})."
        weight = domain_info['weight']
    elif domain_info["weight"] == 0:
        verdict = "⚠️ <b>СРЕДНЯЯ ДОСТОВЕРНОСТЬ</b>"
        reason = "Домен не входит в список эталонных."
        weight = 30
    else:
        verdict = "⚠️ <b>ИСТОЧНИК НЕ В БЕЛОМ СПИСКЕ</b>"
        reason = "Домен не является авторитетным."
        weight = domain_info['weight']

    response_text = (
        f"{verdict}\n\n"
        f"🔗 <b>Ссылка:</b> {url}\n"
        f"📊 <b>Оценка доверия:</b> {weight}/100\n\n"
        f"📝 <b>Почему:</b>\n{reason}\n\n"
    )
    
    # Если нашли миф — добавляем предупреждение
    if myth_warning:
        response_text += f"🚨 <b>ВНИМАНИЕ! В тексте найдена потенциально ложная информация:</b>\n{myth_warning}\n\n"
        
    response_text += (
        f"📖 <b>Фрагмент статьи:</b>\n<i>{text[:300]}...</i>\n\n"
        f"⚠️ <i>Помните: я анализирую авторитетность источника и ищу известные мифы.</i>"
    )

    await message.answer(response_text, parse_mode="HTML", reply_markup=after_answer_kb())
    await state.clear()