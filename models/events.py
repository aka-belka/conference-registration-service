class Event:
    def __init__(
        self,
        event_id: int,
        title: str,
        event_date: str,
        max_seats: int,
        registered: int = 0,
    ) -> None:
        self.id = event_id
        self.title = title
        self.date = event_date
        self.max_seats = max_seats
        self.registered = registered

    def has_free_seats(self) -> bool:
        return self.registered < self.max_seats

    def is_suitable_for(self, min_seats: int) -> bool:
        return self.max_seats >= min_seats

    def __str__(self) -> str:
        return (
            f"{self.title} ({self.date}), "
            f"{self.registered}/{self.max_seats} мест"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Event":
        return cls(
            event_id=data["id"],
            title=data["title"],
            event_date=data["date"],
            max_seats=data["max_seats"],
            registered=data.get("registered", 0),
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "max_seats": self.max_seats,
            "registered": self.registered,
        }

    @staticmethod
    def validate_seats(max_seats: int) -> bool:
        return max_seats > 0


def add_event(events: list[Event], title: str, event_date: str, max_seats: int) -> Event | None:
    if not Event.validate_seats(max_seats):
        print("Ошибка: количество мест должно быть положительным.")
        return None
    event_id = len(events) + 1
    event = Event(event_id, title, event_date, max_seats)
    events.append(event)
    return event


def find_event_by_id(events: list[Event], event_id: int) -> Event | None:
    for event in events:
        if event.id == event_id:
            return event
    return None


def find_events_by_title(events: list[Event], query: str) -> list[Event]:
    query_lower = query.lower()
    return [e for e in events if query_lower in e.title.lower()]


def filter_events_by_seats(events: list[Event], min_seats: int) -> list[Event]:
    return [event for event in events if event.is_suitable_for(min_seats)]


def sort_events_by_date(events: list[Event]) -> list[Event]:
    return sorted(events, key=lambda e: e.date)


def show_events(events: list[Event]) -> None:
    if not events:
        print("Список мероприятий пуст.")
        return
    print(f"{'ID':<5}{'Название':<30}{'Дата':<15}{'Мест':<8}{'Занято':<8}")
    print("-" * 70)
    for e in events:
        print(
            f"{e.id:<5}{e.title:<30}{e.date:<15}"
            f"{e.max_seats:<8}{e.registered:<8}"
        )
