from models.events import add_event
from models.participants import add_participant
from models.tickets import is_ticket_available, create_ticket, cancel_ticket


def _setup():
    events, participants, tickets = [], [], []
    add_event(events, "Хакатон MAX", "20.11.2026", 100)
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    add_participant(participants, "Берг Ксения", "berg_ks@mail.com")
    return events, participants, tickets


def test_ticket_creation():
    events, participants, tickets = _setup()
    ticket = create_ticket(tickets, events, 1, 1, participants)
    assert ticket is not None
    assert ticket.status == "забронирован"
    assert ticket.event is events[0]
    assert ticket.participant is participants[0]
    assert events[0].registered == 1


def test_duplicate_ticket_forbidden():
    events, participants, tickets = _setup()
    create_ticket(tickets, events, 1, 1, participants)
    assert not is_ticket_available(tickets, 1, 1)


def test_cancel_ticket():
    events, participants, tickets = _setup()
    ticket = create_ticket(tickets, events, 1, 1, participants)
    assert cancel_ticket(tickets, events, ticket.id)
    assert ticket.status == "отменён"
    assert events[0].registered == 0
    # отменённый билет не блокирует регистрацию
    assert is_ticket_available(tickets, 1, 1)


def test_no_seats_available():
    events, participants, tickets = _setup()
    events[0].max_seats = 1
    create_ticket(tickets, events, 1, 1, participants)
    assert create_ticket(tickets, events, 1, 2, participants) is None
