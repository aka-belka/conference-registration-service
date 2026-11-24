
import pytest

from events.forms import TicketFilterForm, TicketForm
from events.models import Event, Ticket
from participants.models import Participant


@pytest.fixture
def event(db):
    return Event.objects.create(
        title="Хакатон MAX",
        date="2026-11-20",
        max_seats=2,
    )


@pytest.fixture
def second_event(db):
    return Event.objects.create(
        title="Научная конференция",
        date="2026-12-10",
        max_seats=5,
    )


@pytest.fixture
def participant(db):
    return Participant.objects.create(
        name="Бельская Валерия",
        email="valeria@example.com",
    )


@pytest.fixture
def second_participant(db):
    return Participant.objects.create(
        name="Берг Ксения",
        email="ksenia@example.com",
    )


def test_ticket_filter_form_valid(event):
    form = TicketFilterForm(data={
        "event": event.pk,
        "status": Ticket.Status.BOOKED,
        "event_date": "2026-11-20",
        "ordering": "number",
    })

    assert form.is_valid()
    assert form.cleaned_data["event"] == event
    assert form.cleaned_data["status"] == Ticket.Status.BOOKED


def test_ticket_filter_form_invalid_date():
    form = TicketFilterForm(data={
        "event_date": "не дата",
    })

    assert not form.is_valid()
    assert "event_date" in form.errors


def test_ticket_form_creates_ticket(event, participant):
    form = TicketForm(data={
        "event": event.pk,
        "participant": participant.pk,
        "number": "TICKET-001",
        "status": Ticket.Status.BOOKED,
    })

    assert form.is_valid(), form.errors

    ticket = form.save()

    assert ticket.event == event
    assert ticket.participant == participant
    assert ticket.number == "TICKET-001"
    assert ticket.status == Ticket.Status.BOOKED


def test_ticket_form_rejects_duplicate_active_ticket(
    event,
    participant,
):
    Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.BOOKED,
    )

    form = TicketForm(data={
        "event": event.pk,
        "participant": participant.pk,
        "number": "TICKET-002",
        "status": Ticket.Status.BOOKED,
    })

    assert not form.is_valid()
    assert (
        "У этого участника уже есть активный билет "
        "на выбранное мероприятие."
        in str(form.errors)
    )


def test_ticket_form_rejects_ticket_when_no_seats(
    event,
    participant,
    second_participant,
):
    event.max_seats = 1
    event.save()

    Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.PAID,
    )

    form = TicketForm(data={
        "event": event.pk,
        "participant": second_participant.pk,
        "number": "TICKET-002",
        "status": Ticket.Status.BOOKED,
    })

    assert not form.is_valid()
    assert (
        "На выбранное мероприятие больше нет свободных мест."
        in str(form.errors)
    )


def test_cancelled_ticket_does_not_block_new_ticket(
    event,
    participant,
    second_participant,
):
    event.max_seats = 1
    event.save()

    Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.CANCELLED,
    )

    form = TicketForm(data={
        "event": event.pk,
        "participant": second_participant.pk,
        "number": "TICKET-002",
        "status": Ticket.Status.BOOKED,
    })

    assert form.is_valid(), form.errors


def test_ticket_form_edit_does_not_change_participant(
    event,
    participant,
    second_event,
):
    ticket = Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.BOOKED,
    )

    form = TicketForm(
        data={
            "event": second_event.pk,
            "number": "TICKET-UPDATED",
            "status": Ticket.Status.PAID,
        },
        instance=ticket,
    )

    assert "participant" not in form.fields
    assert form.is_valid(), form.errors

    updated_ticket = form.save()

    assert updated_ticket.event == second_event
    assert updated_ticket.participant == participant
    assert updated_ticket.number == "TICKET-UPDATED"
    assert updated_ticket.status == Ticket.Status.PAID


def test_ticket_form_edit_does_not_count_itself_as_duplicate(
    event,
    participant,
):
    ticket = Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.BOOKED,
    )

    form = TicketForm(
        data={
            "event": event.pk,
            "number": "TICKET-001-EDITED",
            "status": Ticket.Status.PAID,
        },
        instance=ticket,
    )

    assert form.is_valid(), form.errors


def test_ticket_form_rejects_duplicate_number(
    event,
    participant,
    second_participant,
):
    Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.BOOKED,
    )

    form = TicketForm(data={
        "event": event.pk,
        "participant": second_participant.pk,
        "number": "TICKET-001",
        "status": Ticket.Status.BOOKED,
    })

    assert not form.is_valid()
    assert "number" in form.errors
