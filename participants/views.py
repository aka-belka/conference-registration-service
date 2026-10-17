from django.shortcuts import render

from storage import load_participants


def participants(request):
    template = 'participants/participant_list.html'
    participants_list = load_participants()
    context = {
        "participants": participants_list,
    }
    return render(request, template, context)


def participant_detail(request, participant_id: int):
    template = 'participants/participant_detail.html'
    participants_list = load_participants()
    participant = next(
        (p for p in participants_list if p.id == participant_id), None
    )

    context = {
        "participant": participant,
    }
    return render(request, template, context, status=404 if participant is None else 200)
