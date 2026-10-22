import os
from groq import Groq

# Ключ будет браться из переменных окружения
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_video(video_path: str) -> str | None:
    """Распознает речь из видео через Groq API."""
    try:
        with open(video_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(video_path), file.read()),
                model="whisper-large-v3-turbo",
                language="ru",
                response_format="text"
            )
        return transcription.strip()
    except Exception as e:
        print(f"Ошибка распознавания видео (Groq): {e}")
        return None