def add_event(events: list[dict], title: str, event_date: str, max_seats: int) -> dict:
    event_id = len(events) + 1
    event = {
        "id": event_id,
        "title": title,
        "date": event_date,
        "max_seats": max_seats,
        "registered": 0,
    }
    events.append(event)
    return event


def find_event_by_id(events: list[dict], event_id: int) -> dict | None:
    for event in events:
        if event["id"] == event_id:
            return event
    return None


def find_events_by_title(events: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [e for e in events if query_lower in e["title"].lower()]


def filter_events_by_seats(events: list[dict], min_seats: int) -> list[dict]:
    return [event for event in events if event["max_seats"] >= min_seats]


def sort_events_by_date(events: list[dict]) -> list[dict]:
    return sorted(events, key=lambda e: e["date"])


def check_event_capacity(event: dict, min_seats: int) -> bool:
    return event["max_seats"] >= min_seats


def show_events(events: list[dict]) -> None:
    if not events:
        print("Список мероприятий пуст.")
        return
    print(f"{'ID':<5}{'Название':<30}{'Дата':<15}{'Мест':<8}{'Занято':<8}")
    print("-" * 70)
    for event in events:
        print(
            f"{event['id']:<5}{event['title']:<30}{event['date']:<15}"
            f"{event['max_seats']:<8}{event['registered']:<8}"
        )
