from events import find_event_by_id


def is_ticket_available(tickets: list[dict], event_id: int, participant_id: int) -> bool:
    for ticket in tickets:
        if ticket["event_id"] == event_id and ticket["participant_id"] == participant_id:
            return False
    return True


def create_ticket(tickets: list[dict], events: list[dict],
                  event_id: int, participant_id: int) -> dict | None:
    event = find_event_by_id(events, event_id)
    if event is None:
        print("Ошибка: мероприятие не найдено.")
        return None
    if event["registered"] >= event["max_seats"]:
        print("Отказ: свободных мест нет.")
        return None
    if not is_ticket_available(tickets, event_id, participant_id):
        print("Отказ: участник уже зарегистрирован на это мероприятие.")
        return None

    ticket_id = len(tickets) + 1
    ticket = {
        "id": ticket_id,
        "event_id": event_id,
        "participant_id": participant_id,
        "status": "забронирован",
        "number": f"TICKET-{ticket_id:04d}",
    }
    tickets.append(ticket)
    event["registered"] += 1
    return ticket


def cancel_ticket(tickets: list[dict], events: list[dict], ticket_id: int) -> bool:
    for index, ticket in enumerate(tickets):
        if ticket["id"] == ticket_id:
            event = find_event_by_id(events, ticket["event_id"])
            if event is not None and event["registered"] > 0:
                event["registered"] -= 1
            tickets.pop(index)
            return True
    return False


def change_ticket_status(ticket: dict, new_status: str) -> bool:
    allowed = ["забронирован", "оплачен", "отменён"]
    if new_status not in allowed:
        print(f"Ошибка: статус «{new_status}» недопустим.")
        return False
    ticket["status"] = new_status
    return True


def show_tickets(tickets: list[dict], events: list[dict],
                 participants: list[dict]) -> None:
    if not tickets:
        print("Список билетов пуст.")
        return
    print(f"{'ID':<5}{'Номер':<15}{'Мероприятие':<30}{'Участник':<25}{'Статус':<15}")
    print("-" * 90)
    for ticket in tickets:
        event = find_event_by_id(events, ticket["event_id"])
        participant = next(
            (p for p in participants if p["id"] == ticket["participant_id"]), None
        )
        event_title = event["title"] if event else "—"
        participant_name = participant["name"] if participant else "—"
        print(
            f"{ticket['id']:<5}{ticket['number']:<15}{event_title:<30}"
            f"{participant_name:<25}{ticket['status']:<15}"
        )


def get_booking_status(is_available: bool) -> str:
    if is_available:
        return "Регистрация доступна"
    return "Регистрация невозможна"
