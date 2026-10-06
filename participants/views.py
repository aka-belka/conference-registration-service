from django.http import HttpResponse

from homepage.views import page
from storage import load_participants


def participants(request):
    items = ""
    for p in load_participants():
        text = f"{p.name} — {p.email}"
        items += f'<li class="list-group-item">{text}</li>'
    content = f"""
    <h1>Участники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Участники", content))


def participant_detail(request, participant_id: int):
    participants_list = load_participants()
    participant = next(
        (p for p in participants_list if p.id == participant_id), None
    )
    if participant is None:
        content = """
        <h1 class="text-danger">Участник не найден</h1>
        <a href="/participants/" class="btn btn-outline-secondary">
            к списку участников
        </a>
        """
        return HttpResponse(
            page("Участник не найден", content), status=404
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{participant.name}</h5>
            <p class="card-text"><strong>ID:</strong> {participant.id}</p>
            <p class="card-text"><strong>Email:</strong> {participant.email}</p>
            <a href="/participants/" class="btn btn-outline-secondary">
                к списку участников
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(participant.name, content))
