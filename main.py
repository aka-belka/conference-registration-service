from storage import (
    load_participants, save_participants,
    load_events, save_events,
    load_tickets, save_tickets,
)
from participants import (
    add_participant, find_participants_by_name,
    sort_participants_by_name, show_participants,
)
from events import (
    add_event, find_events_by_title,
    filter_events_by_seats, sort_events_by_date, show_events,
)
from tickets import (
    is_ticket_available, create_ticket, cancel_ticket,
    change_ticket_status, show_tickets, get_booking_status,
)
from utils import input_int, input_date, input_non_empty, input_email


def menu() -> None:
    print("\n=== Сервис регистрации участников конференции ===")
    print("1. Показать участников")
    print("2. Добавить участника")
    print("3. Найти участника по имени")
    print("4. Показать мероприятия")
    print("5. Добавить мероприятие")
    print("6. Найти мероприятие по названию")
    print("7. Отобрать мероприятия по числу мест")
    print("8. Зарегистрировать участника на мероприятие")
    print("9. Отменить билет")
    print("10. Изменить статус билета")
    print("11. Показать билеты")
    print("12. Проверить доступность регистрации")
    print("0. Выход")


def handle_choice(choice: int, participants: list[dict], events: list[dict], tickets: list[dict]) -> bool:
    if choice == 0:
        return False
    elif choice == 1:
        show_participants(sort_participants_by_name(participants))
    elif choice == 2:
        name = input_non_empty("Имя участника: ")
        email = input_email("Email: ")
        add_participant(participants, name, email)
        save_participants(participants)
        print("Участник добавлен.")
    elif choice == 3:
        query = input_non_empty("Подстрока имени: ")
        found = find_participants_by_name(participants, query)
        show_participants(found)
    elif choice == 4:
        show_events(sort_events_by_date(events))
    elif choice == 5:
        title = input_non_empty("Название мероприятия: ")
        event_date = input_date("Дата (ДД.ММ.ГГГГ): ").strftime("%d.%m.%Y")
        max_seats = input_int("Максимум мест: ")
        add_event(events, title, event_date, max_seats)
        save_events(events)
        print("Мероприятие добавлено.")
    elif choice == 6:
        query = input_non_empty("Подстрока названия: ")
        show_events(find_events_by_title(events, query))
    elif choice == 7:
        min_seats = input_int("Минимальное число мест: ")
        show_events(filter_events_by_seats(events, min_seats))
    elif choice == 8:
        participant_id = input_int("ID участника: ")
        event_id = input_int("ID мероприятия: ")
        ticket = create_ticket(tickets, events, event_id, participant_id)
        if ticket:
            save_tickets(tickets)
            save_events(events)
            print(f"Билет создан: {ticket['number']}")
    elif choice == 9:
        ticket_id = input_int("ID билета: ")
        if cancel_ticket(tickets, events, ticket_id):
            save_tickets(tickets)
            save_events(events)
            print("Билет отменён.")
        else:
            print("Билет не найден.")
    elif choice == 10:
        ticket_id = input_int("ID билета: ")
        new_status = input_non_empty("Новый статус: ")
        for ticket in tickets:
            if ticket["id"] == ticket_id:
                if change_ticket_status(ticket, new_status):
                    save_tickets(tickets)
                    print("Статус изменён.")
                break
        else:
            print("Билет не найден.")
    elif choice == 11:
        show_tickets(tickets, events, participants)
    elif choice == 12:
        participant_id = input_int("ID участника: ")
        event_id = input_int("ID мероприятия: ")
        available = is_ticket_available(tickets, event_id, participant_id)
        print(get_booking_status(available))
    else:
        print("Неизвестный пункт меню.")
    return True


def main() -> None:
    participants = load_participants()
    events = load_events()
    tickets = load_tickets()

    while True:
        menu()
        choice = input_int("Выберите действие: ")
        if not handle_choice(choice, participants, events, tickets):
            print("Выход")
            break


if __name__ == "__main__":
    main()
