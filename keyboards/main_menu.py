from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def consent_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Согласен", callback_data="consent_yes")
    builder.button(text="❌ Отказаться", callback_data="consent_no")
    return builder.as_markup()

def after_answer_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Новый запрос", callback_data="new_request")
    builder.button(text="🔗 Проверить ссылку", callback_data="check_link")
    builder.button(text="🔍 Проверить факт", callback_data="check_fact")
    builder.button(text="📸 Проверить фото", callback_data="check_photo")
    builder.button(text="🎥 Проверить видео", callback_data="check_video") # НОВАЯ КНОПКА
    builder.button(text="❓ Помощь", callback_data="help")
    builder.adjust(1, 2, 2, 1) 
    return builder.as_markup()

def start_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🩺 Описать симптомы", callback_data="action_symptoms")
    builder.button(text="🔗 Проверить ссылку", callback_data="action_link")
    builder.button(text="🔍 Проверить факт", callback_data="action_fact")
    builder.button(text="📸 Проверить фото", callback_data="action_photo")
    builder.button(text="🎥 Проверить видео", callback_data="action_video") # НОВАЯ КНОПКА
    builder.adjust(1) 
    return builder.as_markup()