from datetime import date

name = "Бельская Валерия"
email = "sergeevnau18@gmail.com"
event_title = "Хакатон MAX"
event_date = date(2026, 9, 15)
event_max_seats = 100
ticket_number = "TICKET-0001"
ticket_status = "забронирован"
registered_count = 99


def register(name, email):
    if "@" not in email:
        return "Некорректный email!"
    if name.strip() == "":
        return "Имя не может быть пустым!"
    return f"Участник {name} зарегистрирован с email {email}"


def create_event(title, event_date, max_seats):
    if max_seats <= 0:
        return "Количество мест должно быть положительным!"
    return (f"Мероприятие «{title}» создано на {event_date}. Количество мест: {max_seats}")


def book_ticket(registered, max_seats):
    if registered >= max_seats:
        return "Свободных мест нет!", registered
    registered += 1
    return "Билет успешно забронирован", registered


def change_ticket_status(current_status, new_status):
    allowed = ["забронирован", "оплачен", "отменён"]
    if new_status not in allowed:
        return f"Статус '{new_status}' недопустим!"
    if current_status == new_status:
        return f"Статус уже '{current_status}', изменение не требуется!"
    return f"Статус билета изменён c '{current_status}' на '{new_status}'"


def show_participants(participants):
    if len(participants) == 0:
        return "Список участников пуст"
    return "Участники: " + ", ".join(participants)


print(create_event(event_title, event_date, event_max_seats))

print(register(name, email))

message, registered_count = book_ticket(registered_count, event_max_seats)
print(message)
print(f"Всего зарегистрировано: {registered_count} из {event_max_seats}")

print(change_ticket_status(ticket_status, "оплачен"))

participants = [name, "Бельская Татьяна", "Петрова Александра"]
print(show_participants(participants))

print(f"Номер билета: {ticket_number}")
print(f"Дата мероприятия: {event_date}")
