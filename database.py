import json
import os

DB_FILE = "data.json"


# =====================================================
# 📦 ИНИЦИАЛИЗАЦИЯ БАЗЫ
# =====================================================

def create_database():
    if not os.path.exists(DB_FILE):
        data = {
            "players": {},
            "poll": {},
            "answers": {}
        }

        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


# =====================================================
# 📖 БЕЗОПАСНАЯ ЗАГРУЗКА
# =====================================================

def load_data():
    create_database()

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            # защита от битого JSON
            if not isinstance(data, dict):
                raise ValueError("Invalid DB format")

            data.setdefault("players", {})
            data.setdefault("poll", {})
            data.setdefault("answers", {})

            return data

    except (json.JSONDecodeError, ValueError):
        # если файл сломан — восстанавливаем
        data = {
            "players": {},
            "poll": {},
            "answers": {}
        }

        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data


# =====================================================
# 💾 СОХРАНЕНИЕ
# =====================================================

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# =====================================================
# 👥 ИГРОКИ
# =====================================================

def add_player(user_id, name):
    data = load_data()

    data["players"][str(user_id)] = {
        "name": name
    }

    save_data(data)


def player_exists(user_id):
    data = load_data()
    return str(user_id) in data["players"]


def get_player(user_id):
    data = load_data()
    return data["players"].get(str(user_id))


def get_all_players():
    data = load_data()
    return data["players"]


# =====================================================
# 📢 ОПРОС
# =====================================================

def create_poll(date, time, place):
    data = load_data()

    data["poll"] = {
        "date": date,
        "time": time,
        "place": place
    }

    data["answers"] = {}  # сброс ответов

    save_data(data)


def get_poll():
    data = load_data()
    return data.get("poll", {})


# =====================================================
# 🏒 ОТВЕТЫ
# =====================================================

def save_attendance(user_id, attendance):
    data = load_data()

    uid = str(user_id)

    if uid not in data["answers"]:
        data["answers"][uid] = {}

    data["answers"][uid]["attendance"] = attendance

    save_data(data)


def save_payment(user_id, payment):
    data = load_data()

    uid = str(user_id)

    if uid not in data["answers"]:
        data["answers"][uid] = {}

    data["answers"][uid]["payment"] = payment

    save_data(data)


def get_answers():
    data = load_data()
    return data.get("answers", {})


def get_user_answer(user_id):
    data = load_data()
    return data.get("answers", {}).get(str(user_id))