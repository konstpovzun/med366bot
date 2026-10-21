import requests
from bs4 import BeautifulSoup
import re
from core.facts_db import FACTS_DB # Импортируем базу фактов

def extract_text_from_url(url: str) -> str | None:
    """Скачивает страницу и вытаскивает основной текст."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.decompose()

        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
        text = ' '.join([p.get_text() for p in paragraphs])
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) < 50:
            return None
            
        return text[:3000] # Берем больше текста для анализа
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return None

def analyze_text_for_myths(text: str) -> str | None:
    """Ищет в тексте известные мифы из нашей базы."""
    text_lower = text.lower()
    found_myths = []
    
    for fact in FACTS_DB:
        # Если в тексте есть ключевые слова из нашего мифа (например, "антибиотик" и "вирус")
        if any(kw in text_lower for kw in fact["keywords"]):
            # Проверяем, не является ли это просто упоминанием (упрощенно)
            found_myths.append(fact["verdict"] + " " + fact["explanation"][:50] + "...")
            
    if found_myths:
        return "\n".join(found_myths)
    return None