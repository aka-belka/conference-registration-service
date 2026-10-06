from django.http import HttpResponse

from homepage.views import page
from storage import load_events, load_participants, load_tickets


def events(request):
    items = ""
    for e in load_events():
        text = f"{e.title} — {e.date}, мест: {e.max_seats}"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/events/{e.id}/">{text}</a></li>'
        )
    content = f"""
    <h1>Мероприятия</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Мероприятия", content))


def tickets(request):
    events_list = load_events()
    participants_list = load_participants()
    tickets_list = load_tickets(events_list, participants_list)

    items = ""
    for t in tickets_list:
        text = f"{t.number}: {t.participant.name} → {t.event.title} [{t.status}]"
        items += f'<li class="list-group-item">{text}</li>'

    content = f"""
    <h1>Билеты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Билеты", content))


def event_detail(request, event_id: int):
    events_list = load_events()
    event = next(
        (e for e in events_list if e.id == event_id), None
    )
    if event is None:
        content = """
        <h1 class="text-danger">Мероприятие не найдено</h1>
        <a href="/events/" class="btn btn-outline-secondary">
            к списку мероприятий
        </a>
        """
        return HttpResponse(
            page("Мероприятие не найдено", content), status=404
        )

    status = "есть места" if event.has_free_seats() else "мест нет"
    badge = "bg-success" if event.has_free_seats() else "bg-danger"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{event.title}</h5>
            <p class="card-text"><strong>ID:</strong> {event.id}</p>
            <p class="card-text"><strong>Дата:</strong> {event.date}</p>
            <p class="card-text">
                <strong>Мест:</strong> {event.registered}/{event.max_seats}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/events/" class="btn btn-outline-secondary">
                к списку мероприятий
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(event.title, content))
