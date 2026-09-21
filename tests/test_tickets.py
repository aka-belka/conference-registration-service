from events import add_event
from tickets import is_ticket_available, create_ticket, cancel_ticket


def test_is_ticket_available_empty():
    tickets = []
    assert is_ticket_available(tickets, 1, 1)


def test_create_ticket():
    events = []
    tickets = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    ticket = create_ticket(tickets, events, 1, 1)
    assert ticket is not None
    assert ticket["status"] == "забронирован"
    assert events[0]["registered"] == 1


def test_duplicate_ticket_forbidden():
    events = []
    tickets = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    create_ticket(tickets, events, 1, 1)
    assert not is_ticket_available(tickets, 1, 1)


def test_cancel_ticket():
    events = []
    tickets = []
    add_event(events, "Kokos хаккатон", "12.10.2026", 100)
    create_ticket(tickets, events, 1, 1)
    assert cancel_ticket(tickets, events, 1)
    assert len(tickets) == 0
    assert events[0]["registered"] == 0


def test_no_seats_available():
    events = []
    tickets = []
    add_event(events, "Учебная олимпиада", "12.10.2026", 1)
    create_ticket(tickets, events, 1, 1)
    assert create_ticket(tickets, events, 1, 2) is None
