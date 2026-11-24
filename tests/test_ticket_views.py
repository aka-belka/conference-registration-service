
import pytest

from django.urls import reverse

from events.models import Event, Ticket
from participants.models import Participant

pytestmark = pytest.mark.django_db


@pytest.fixture
def event(db):
    return Event.objects.create(
        title="Хакатон MAX",
        date="2026-11-20",
        max_seats=2,
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


@pytest.fixture
def ticket(event, participant):
    return Ticket.objects.create(
        event=event,
        participant=participant,
        number="TICKET-001",
        status=Ticket.Status.BOOKED,
    )


def test_ticket_create_get(client):
    response = client.get(reverse("ticket_create"))

    assert response.status_code == 200
    assert "form" in response.context


def test_ticket_create_post(client, event, participant):
    response = client.post(
        reverse("ticket_create"),
        {
            "event": event.pk,
            "participant": participant.pk,
            "number": "TICKET-NEW",
            "status": Ticket.Status.BOOKED,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("tickets")

    created_ticket = Ticket.objects.get(number="TICKET-NEW")

    assert created_ticket.event == event
    assert created_ticket.participant == participant


def test_ticket_create_invalid_post(client, event):
    response = client.post(
        reverse("ticket_create"),
        {
            "event": event.pk,
            "participant": "",
            "number": "",
            "status": Ticket.Status.BOOKED,
        },
    )

    assert response.status_code == 200
    assert response.context["form"].errors
    assert Ticket.objects.count() == 0


def test_ticket_update_get(client, ticket):
    response = client.get(
        reverse("ticket_update", args=[ticket.pk])
    )

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].instance == ticket


def test_ticket_update_post(client, ticket, event):
    response = client.post(
        reverse("ticket_update", args=[ticket.pk]),
        {
            "event": event.pk,
            "number": "TICKET-UPDATED",
            "status": Ticket.Status.PAID,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("tickets")

    ticket.refresh_from_db()

    assert ticket.number == "TICKET-UPDATED"
    assert ticket.status == Ticket.Status.PAID


def test_ticket_update_keeps_participant(
    client,
    ticket,
    second_participant,
):
    response = client.post(
        reverse("ticket_update", args=[ticket.pk]),
        {
            "event": ticket.event.pk,
            "number": "TICKET-UPDATED",
            "status": Ticket.Status.PAID,
            "participant": second_participant.pk,
        },
    )

    assert response.status_code == 302

    ticket.refresh_from_db()

    assert ticket.participant_id != second_participant.pk


def test_ticket_cancel_post(client, ticket):
    response = client.post(
        reverse("ticket_cancel", args=[ticket.pk])
    )

    assert response.status_code == 302
    assert response.url == reverse("tickets")

    ticket.refresh_from_db()

    assert ticket.status == Ticket.Status.CANCELLED
    assert Ticket.objects.filter(pk=ticket.pk).exists()


def test_ticket_cancel_get_not_allowed(client, ticket):
    response = client.get(
        reverse("ticket_cancel", args=[ticket.pk])
    )

    assert response.status_code == 405

    ticket.refresh_from_db()

    assert ticket.status == Ticket.Status.BOOKED


def test_ticket_cancel_does_not_cancel_twice(client, ticket):
    ticket.status = Ticket.Status.CANCELLED
    ticket.save()

    response = client.post(
        reverse("ticket_cancel", args=[ticket.pk])
    )

    assert response.status_code == 302

    ticket.refresh_from_db()

    assert ticket.status == Ticket.Status.CANCELLED


def test_ticket_update_returns_404_for_missing_ticket(client):
    response = client.get(
        reverse("ticket_update", args=[99999])
    )

    assert response.status_code == 404


def test_ticket_cancel_returns_404_for_missing_ticket(client):
    response = client.post(
        reverse("ticket_cancel", args=[99999])
    )

    assert response.status_code == 404


def test_tickets_page_displays_filter_form(client):
    response = client.get(reverse("tickets"))

    assert response.status_code == 200
    assert "form" in response.context


def test_tickets_page_filters_by_status(client, ticket):
    paid_ticket = Ticket.objects.create(
        event=ticket.event,
        participant=Participant.objects.create(
            name="Берг Ксения",
            email="ksenia@example.com",
        ),
        number="TICKET-002",
        status=Ticket.Status.PAID,
    )

    response = client.get(
        reverse("tickets"),
        {"status": Ticket.Status.PAID},
    )

    assert response.status_code == 200
    displayed_tickets = list(response.context["tickets"])

    assert paid_ticket in displayed_tickets
    assert ticket not in displayed_tickets
