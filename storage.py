import json
import os
from typing import Any

DATA_DIR = "data"


def _ensure_data_dir() -> None:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _load_json(filename: str, default: Any) -> Any:
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Предупреждение: файл {filename} повреждён, данные сброшены.")
        return default


def _save_json(filename: str, data: Any) -> None:
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_participants() -> list[dict]:
    return _load_json("participants.json", [])


def save_participants(participants: list[dict]) -> None:
    _save_json("participants.json", participants)


def load_events() -> list[dict]:
    return _load_json("events.json", [])


def save_events(events: list[dict]) -> None:
    _save_json("events.json", events)


def load_tickets() -> list[dict]:
    return _load_json("tickets.json", [])


def save_tickets(tickets: list[dict]) -> None:
    _save_json("tickets.json", tickets)
