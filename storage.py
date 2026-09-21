import json
import os
from typing import Any
from models import Event, Participant, Ticket

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


def load_participants() -> list[Participant]:
    raw = _load_json("participants.json", [])
    return [Participant.from_data(item) for item in raw]


def save_participants(participants: list[Participant]) -> None:
    _save_json("participants.json", [p.to_data() for p in participants])


def load_events() -> list[Event]:
    raw = _load_json("events.json", [])
    return [Event.from_data(item) for item in raw]


def save_events(events: list[Event]) -> None:
    _save_json("events.json", [e.to_data() for e in events])


def load_tickets(
    events: list[Event],
    participants: list[Participant],
) -> list[Ticket]:
    raw = _load_json("tickets.json", [])
    tickets: list[Ticket] = []
    for item in raw:
        ticket = Ticket.from_data(item, events, participants)
        if ticket is not None:
            tickets.append(ticket)
    return tickets


def save_tickets(tickets: list[Ticket]) -> None:
    _save_json("tickets.json", [t.to_data() for t in tickets])
