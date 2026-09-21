from .events import Event, find_event_by_id
from .participants import Participant


class Ticket:

    ALLOWED_STATUSES = ("забронирован", "оплачен", "отменён")

    def __init__(
        self,
        ticket_id: int,
        event: Event,
        participant: Participant,
        status: str = "забронирован",
        number: str | None = None,
    ) -> None:
        self.id = ticket_id
        self.event = event
        self.participant = participant
        self.status = status
        self.number = number if number else f"TICKET-{ticket_id:04d}"

    def cancel(self) -> None:
        self.status = "отменён"

    def change_status(self, new_status: str) -> bool:
        if new_status not in self.ALLOWED_STATUSES:
            print(f"Ошибка: статус «{new_status}» недопустим.")
            return False
        self.status = new_status
        return True

    def __str__(self) -> str:
        return (
            f"{self.number}: {self.participant.name} → "
            f"{self.event.title} [{self.status}]"
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
        events: list[Event],
        participants: list[Participant],
    ) -> "Ticket | None":
        event = find_event_by_id(events, data["event_id"])
        participant = next(
            (p for p in participants if p.id == data["participant_id"]), None
        )
        if event is None or participant is None:
            return None
        return cls(
            ticket_id=data["id"],
            event=event,
            participant=participant,
            status=data["status"],
            number=data["number"],
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "event_id": self.event.id,
            "participant_id": self.participant.id,
            "status": self.status,
            "number": self.number,
        }


def is_ticket_available(
    tickets: list[Ticket],
    event_id: int,
    participant_id: int,
) -> bool:
    for ticket in tickets:
        if ticket.event.id == event_id and ticket.participant.id == participant_id:
            if ticket.status != "отменён":
                return False
    return True


def create_ticket(
    tickets: list[Ticket],
    events: list[Event],
    event_id: int,
    participant_id: int,
    participants: list[Participant],
) -> Ticket | None:
    event = find_event_by_id(events, event_id)
    if event is None:
        print("Ошибка: мероприятие не найдено.")
        return None
    if not event.has_free_seats():
        print("Отказ: свободных мест нет.")
        return None
    if not is_ticket_available(tickets, event_id, participant_id):
        print("Отказ: участник уже зарегистрирован на это мероприятие.")
        return None

    participant = next(
        (p for p in participants if p.id == participant_id), None
    )
    if participant is None:
        print("Ошибка: участник не найден.")
        return None

    ticket_id = len(tickets) + 1
    ticket = Ticket(ticket_id, event, participant)
    tickets.append(ticket)
    event.registered += 1
    return ticket


def cancel_ticket(
    tickets: list[Ticket],
    events: list[Event],
    ticket_id: int,
) -> bool:
    for ticket in tickets:
        if ticket.id == ticket_id:
            if ticket.status == "отменён":
                return False
            ticket.cancel()
            if ticket.event.registered > 0:
                ticket.event.registered -= 1
            return True
    return False


def show_tickets(tickets: list[Ticket]) -> None:
    if not tickets:
        print("Список билетов пуст.")
        return
    print(f"{'ID':<5}{'Номер':<15}{'Мероприятие':<30}{'Участник':<25}{'Статус':<15}")
    print("-" * 90)
    for t in tickets:
        print(
            f"{t.id:<5}{t.number:<15}{t.event.title:<30}"
            f"{t.participant.name:<25}{t.status:<15}"
        )


def get_booking_status(is_available: bool) -> str:
    if is_available:
        return "Регистрация доступна"
    return "Регистрация невозможна"
