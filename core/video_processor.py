import whisper
import os

# Загружаем модель Whisper. Для экономии памяти на Railway лучше использовать 'tiny'.
# Если будете запускать локально на мощном ПК, можно 'base' или 'small'.
model = whisper.load_model("tiny")

def transcribe_video(video_path: str) -> str | None:
    """Распознает речь из видеофайла."""
    try:
        result = model.transcribe(video_path, language='ru')
        return result['text'].strip()
    except Exception as e:
        print(f"Ошибка распознавания видео: {e}")
        return None