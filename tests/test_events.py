from events import (
    add_event, find_event_by_id, find_events_by_title,
    filter_events_by_seats, check_event_capacity,
)


def test_add_event():
    events = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    assert len(events) == 1
    assert events[0]["title"] == "Kokos хаккатон"


def test_find_event_by_id():
    events = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    assert find_event_by_id(events, 1) is not None
    assert find_event_by_id(events, 99) is None


def test_find_events_by_title():
    events = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    add_event(events, "Научная конференция", "12.10.2026", 50)
    found = find_events_by_title(events, "kokos")
    assert len(found) == 1


def test_filter_events_by_seats():
    events = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    add_event(events, "Научная конференция", "12.10.2026", 50)
    found = filter_events_by_seats(events, 60)
    assert len(found) == 1
    assert found[0]["title"] == "Kokos хаккатон"


def test_check_event_capacity():
    event = {"id": 1, "title": "Test", "date": "01.01.2026",
             "max_seats": 30, "registered": 0}
    assert check_event_capacity(event, 20)
    assert not check_event_capacity(event, 50)
