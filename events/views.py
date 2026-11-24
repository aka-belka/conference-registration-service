from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.shortcuts import get_object_or_404, redirect, render

from events.models import Event, Ticket
from participants.models import Participant
from django.views.decorators.http import require_POST, require_http_methods

from .forms import TicketFilterForm, TicketForm


def events(request):
    events_list = (
        Event.objects
        .annotate(
            registered_count=Count(
                'tickets',
                filter=~Q(
                    tickets__status=Ticket.Status.CANCELLED
                ),
            )
        )
        .annotate(
            free_seats=F('max_seats') - F('registered_count')
        )
        .order_by('date', 'title')
    )

    paginator = Paginator(events_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "events/event_list.html",
        {
            "events": page_obj.object_list,
            "page_obj": page_obj,
        }
    )


def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.annotate(
            registered_count=Count(
                'tickets',
                filter=~Q(
                    tickets__status=Ticket.Status.CANCELLED
                ),
            )
        ).annotate(
            free_seats=F('max_seats') - F('registered_count')
        ),
        pk=event_id,
    )

    tickets_list = (
        Ticket.objects
        .active()
        .for_event(event.id)
        .select_related('participant', 'event')
        .order_by('number')
    )

    context = {
        "event": event,
        "tickets": tickets_list,
        "free_seats": event.free_seats,
    }

    return render(
        request,
        "events/event_detail.html",
        context
    )


def tickets(request):
    tickets_list = (
        Ticket.objects
        .select_related('event', 'participant')
        .all()
    )

    return render(
        request,
        "events/tickets.html",
        {"tickets": tickets_list}
    )


def search_events(request):
    query = request.GET.get("q", "").strip()
    date_str = request.GET.get("date", "").strip()

    error = None

    events_list = Event.objects.annotate(
        registered_count=Count(
            'tickets',
            filter=~Q(
                tickets__status=Ticket.Status.CANCELLED
            ),
        )
    ).annotate(
        free_seats=F('max_seats') - F('registered_count')
    )

    if query:
        events_list = events_list.filter(
            title__icontains=query
        )

    if date_str:
        try:
            selected_date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            error = "Укажите корректную дату в формате YYYY-MM-DD."

        else:
            events_list = events_list.filter(
                date=selected_date
            )

    events_list = events_list.order_by('date', 'title')

    paginator = Paginator(events_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "events": page_obj.object_list,
        "page_obj": page_obj,
        "search_date": date_str,
        "query": query,
        "error": error,
    }

    return render(
        request,
        "events/search.html",
        context
    )


def statistics(request):
    stats = (
        Event.objects
        .annotate(
            tickets_count=Count(
                'tickets',
                filter=~Q(
                    tickets__status=Ticket.Status.CANCELLED
                ),
            ),
            booked_count=Count(
                'tickets',
                filter=Q(
                    tickets__status=Ticket.Status.BOOKED
                ),
            ),
            paid_count=Count(
                'tickets',
                filter=Q(
                    tickets__status=Ticket.Status.PAID
                ),
            ),
            cancelled_count=Count(
                'tickets',
                filter=Q(
                    tickets__status=Ticket.Status.CANCELLED
                ),
            ),
        )
        .order_by('-tickets_count')
    )

    totals = Ticket.objects.aggregate(
        total_tickets=Count('id'),
        booked_tickets=Count(
            'id',
            filter=Q(status=Ticket.Status.BOOKED)
        ),
        paid_tickets=Count(
            'id',
            filter=Q(status=Ticket.Status.PAID)
        ),
        cancelled_tickets=Count(
            'id',
            filter=Q(status=Ticket.Status.CANCELLED)
        ),
        avg_seats=Avg('event__max_seats'),
        min_seats=Min('event__max_seats'),
        max_seats=Max('event__max_seats'),
    )

    total_registered = Ticket.objects.active().count()

    events_short = (
        Event.objects
        .values('id', 'title', 'date')
        .order_by('date')
    )

    context = {
        "statistics": stats,
        "totals": totals,
        "total_registered": total_registered,
        "events_short": events_short,
    }

    return render(
        request,
        "events/statistics.html",
        context
    )


def tickets_paginated(request):
    form = TicketFilterForm(request.GET or None)

    tickets_qs = (
        Ticket.objects
        .select_related("event", "participant")
    )

    if form.is_valid():
        event = form.cleaned_data.get("event")
        status = form.cleaned_data.get("status")
        event_date = form.cleaned_data.get("event_date")
        ordering = form.cleaned_data.get("ordering") or "number"

        if event:
            tickets_qs = tickets_qs.filter(event=event)

        if status:
            tickets_qs = tickets_qs.filter(status=status)

        if event_date:
            tickets_qs = tickets_qs.filter(
                event__date=event_date
            )

        allowed_ordering = {
            "number",
            "-number",
            "event__date",
            "-event__date",
            "participant__name",
            "-participant__name",
        }

        if ordering not in allowed_ordering:
            ordering = "number"

        tickets_qs = tickets_qs.order_by(ordering)

    paginator = Paginator(tickets_qs, 5)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )

    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()

    context = {
        "form": form,
        "page_obj": page_obj,
        "tickets": page_obj.object_list,
        "query_string": query_string,
    }

    return render(
        request,
        "events/tickets.html",
        context
    )


@require_http_methods(["GET", "POST"])
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("tickets")

    else:
        form = TicketForm()

    return render(
        request,
        "events/ticket_form.html",
        {
            "form": form,
            "title": "Создание билета",
            "button_text": "Создать билет",
        }
    )


@require_http_methods(["GET", "POST"])
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id
    )

    if request.method == "POST":
        form = TicketForm(
            request.POST,
            instance=ticket
        )

        if form.is_valid():
            form.save()
            return redirect("tickets")

    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        "events/ticket_form.html",
        {
            "form": form,
            "title": "Редактирование билета",
            "button_text": "Сохранить изменения",
            "ticket": ticket,
        }
    )


@require_POST
def ticket_cancel(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id
    )

    if ticket.status != Ticket.Status.CANCELLED:
        ticket.status = Ticket.Status.CANCELLED
        ticket.save(update_fields=["status"])

    return redirect("tickets")


def participants_search(request):
    query = request.GET.get('q', '').strip()

    participants_list = Participant.objects.all()

    if query:
        participants_list = participants_list.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
        )

    participants_list = participants_list.order_by('name')

    paginator = Paginator(participants_list, 10)
    page_obj = paginator.get_page(
        request.GET.get('page', 1)
    )

    return render(
        request,
        "participants/participant_list.html",
        {
            "participants": page_obj.object_list,
            "page_obj": page_obj,
            "query": query,
        }
    )
