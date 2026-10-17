from django.shortcuts import render
from storage import load_events, load_participants, load_tickets


def events(request):
    template = 'events/event_list.html'
    events_list = load_events()
    context = {
        "events": events_list,
    }

    return render(request, template, context)


def tickets(request):
    template = 'events/tickets.html'
    events_list = load_events()
    participants_list = load_participants()
    tickets_list = load_tickets(events_list, participants_list)

    context = {
        "tickets": tickets_list
    }

    return render(request, template, context)


def event_detail(request, event_id: int):
    template = 'events/event_detail.html'
    events_list = load_events()
    event = next(
        (e for e in events_list if e.id == event_id), None
    )
    context = {
        "event": event,
    }

    return render(request, template, context, status=404 if event is None else 200)
