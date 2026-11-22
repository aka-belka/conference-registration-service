from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from .models import Event, Ticket


def events(request):
    events_list = Event.objects.all().order_by('date')
    return render(request, "events/event_list.html", {"events": events_list})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tickets_list = event.tickets.select_related('participant').all()
    context = {
        "event": event,
        "tickets": tickets_list,
    }
    return render(request, "events/event_detail.html", context)


def tickets(request):
    tickets_list = (
        Ticket.objects
        .select_related('event', 'participant')
        .all()
    )
    return render(request, "events/tickets.html", {"tickets": tickets_list})


def search_events(request):
    query = request.GET.get("q", "").strip()
    date_str = request.GET.get("date", "").strip()
    error = None
    events_list = Event.objects.all()

    if query:
        events_list = events_list.filter(title__icontains=query)

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату в формате YYYY-MM-DD."
        else:
            events_list = events_list.filter(date=selected_date)

    events_list = events_list.order_by('date', 'title')

    context = {
        "events": events_list,
        "search_date": date_str,
        "query": query,
        "error": error,
    }
    return render(request, "events/search.html", context)


def statistics(request):
    stats = (
        Event.objects
        .annotate(tickets_count=Count('tickets'))
        .order_by('-tickets_count')
    )
    totals = Ticket.objects.aggregate(
        total_tickets=Count('id'),
        avg_seats=Avg('event__max_seats'),
        min_seats=Min('event__max_seats'),
        max_seats=Max('event__max_seats'),
    )
    total_registered = Event.objects.aggregate(
        total=Sum('registered')
    )['total'] or 0

    events_short = Event.objects.values('id', 'title', 'date').order_by('date')

    context = {
        "statistics": stats,
        "totals": totals,
        "total_registered": total_registered,
        "events_short": events_short
    }
    return render(request, "events/statistics.html", context)


def tickets_paginated(request):
    tickets_qs = (
        Ticket.objects
        .select_related('event', 'participant')
        .order_by('number')
    )
    paginator = Paginator(tickets_qs, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "events/tickets.html",
        {"page_obj": page_obj, "tickets": page_obj.object_list},
    )


def active_tickets(request):
    active = (
        Ticket.objects
        .exclude(status='отменён')
        .filter(status__in=['забронирован', 'оплачен'])
        .select_related('event', 'participant')
        .order_by('-id')
    )
    return render(request, "events/tickets.html", {"tickets": active})


def tickets_by_event_status(request):
    event_title = request.GET.get('event', '').strip()
    status = request.GET.get('status', '').strip()

    qs = Ticket.objects.select_related('event', 'participant')
    if event_title:
        qs = qs.filter(event__title__icontains=event_title)
    if status in dict(Ticket.STATUS_CHOICES):
        qs = qs.filter(status=status)

    qs = qs.order_by('event__date', 'participant__name')

    context = {
        "tickets": qs,
        "event_title": event_title,
        "status": status,
        "statuses": Ticket.STATUS_CHOICES,
    }
    return render(request, "events/tickets.html", context)


def participants_search(request):
    from participants.models import Participant
    query = request.GET.get('q', '').strip()
    participants_list = Participant.objects.all()
    if query:
        participants_list = participants_list.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
    participants_list = participants_list.order_by('name')
    return render(
        request,
        "participants/participant_list.html",
        {"participants": participants_list, "query": query},
    )
