from django.shortcuts import get_object_or_404, render

from .models import Participant


def participants(request):
    participants_list = Participant.objects.all().order_by('name')
    return render(
        request,
        "participants/participant_list.html",
        {"participants": participants_list},
    )


def participant_detail(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    tickets_list = participant.tickets.select_related('event').all()
    context = {
        "participant": participant,
        "tickets": tickets_list,
    }
    return render(request, "participants/participant_detail.html", context)
