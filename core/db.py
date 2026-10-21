import json
import os

DB_FILE = "users_db.json"

def load_db() -> dict:
    """Загружает базу из файла."""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_db(data: dict):
    """Сохраняет базу в файл."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_user_profile(user_id: int, age: int, gender: str, weight: float):
    """Сохраняет профиль пользователя."""
    db = load_db()
    db[str(user_id)] = {
        "age": age,
        "gender": gender,
        "weight": weight
    }
    save_db(db)

def get_user_profile(user_id: int) -> dict | None:
    """Возвращает профиль пользователя, если он есть."""
    db = load_db()
    return db.get(str(user_id))