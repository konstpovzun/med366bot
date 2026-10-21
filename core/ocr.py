import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import io

# В облаке Tesseract обычно уже в PATH, но для локального запуска оставим путь
# Если запускаете локально и он не в PATH, раскомментируйте строку ниже и укажите свой путь
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_bytes: bytes) -> str | None:
    """Распознает текст с картинки с предобработкой."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # 1. Оттенки серого
        image = ImageOps.grayscale(image)
        
        # 2. Контраст
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # 3. Бинаризация (черный текст на белом фоне)
        image = image.point(lambda x: 0 if x < 140 else 255, '1')
        
        text = pytesseract.image_to_string(image, lang='rus+eng', config='--psm 3')
        return text.strip()
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return None

def analyze_image_color(image_bytes: bytes) -> str:
    """Анализирует преобладающие цвета (для определения сыпи/ран)."""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image.thumbnail((100, 100))
        pixels = list(image.getdata())
        
        red_pixels = 0
        total_pixels = len(pixels)
        
        for r, g, b in pixels:
            if r > 100 and r > g * 1.5 and r > b * 1.5:
                red_pixels += 1
                
        red_ratio = red_pixels / total_pixels
        if red_ratio > 0.3:
            return "red_dominant"
        return "normal"
    except Exception as e:
        print(f"Ошибка анализа цвета: {e}")
        return "normal"