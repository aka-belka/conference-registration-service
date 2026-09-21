from models import Event
from models.events import (
    add_event, find_event_by_id, find_events_by_title,
    filter_events_by_seats,
)


def test_event_creation():
    e = Event(1, "Хакатон MAX", "20.11.2026", 100)
    assert e.id == 1
    assert e.title == "Хакатон MAX"
    assert e.has_free_seats()
    assert "Хакатон MAX" in str(e)


def test_add_event():
    events = []
    add_event(events, "Хакатон MAX", "20.11.2026", 100)
    assert len(events) == 1
    assert events[0].title == "Хакатон MAX"


def test_find_event_by_id():
    events = []
    add_event(events, "Хакатон MAX", "20.11.2026", 100)
    assert find_event_by_id(events, 1) is not None
    assert find_event_by_id(events, 99) is None


def test_find_events_by_title():
    events = []
    add_event(events, "Хакатон MAX", "20.11.2026", 100)
    add_event(events, "Научная конференция", "12.10.2026", 50)
    found = find_events_by_title(events, "max")
    assert len(found) == 1


def test_filter_events_by_seats():
    events = []
    add_event(events, "Хакатон MAX", "20.11.2026", 100)
    add_event(events, "Научная конференция", "12.10.2026", 50)
    found = filter_events_by_seats(events, 60)
    assert len(found) == 1
    assert found[0].title == "Хакатон MAX"
