import whisper

def transcribe_video(video_path: str) -> str | None:
    try:
        # Загружаем модель ТОЛЬКО в момент обработки видео
        model = whisper.load_model("tiny")
        result = model.transcribe(video_path, language='ru')
        return result['text'].strip()
    except Exception as e:
        print(f"Ошибка распознавания видео: {e}")
        return None