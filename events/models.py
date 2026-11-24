from django.db import models
from participants.models import Participant


class Event(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )

    date = models.DateField(
        verbose_name="Дата"
    )

    max_seats = models.IntegerField(
        verbose_name="Максимум мест"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['date', 'title']


class TicketQuerySet(models.QuerySet):

    def booked(self):
        return self.filter(
            status=self.model.Status.BOOKED
        )

    def paid(self):
        return self.filter(
            status=self.model.Status.PAID
        )

    def cancelled(self):
        return self.filter(
            status=self.model.Status.CANCELLED
        )

    def active(self):
        return self.filter(
            status__in=[
                self.model.Status.BOOKED,
                self.model.Status.PAID,
            ]
        )

    def for_date(self, selected_date):
        return self.filter(
            event__date=selected_date
        )

    def for_event(self, event_id):
        return self.filter(
            event_id=event_id
        )


class TicketManager(
    models.Manager.from_queryset(TicketQuerySet)
):
    pass


class Ticket(models.Model):

    class Status(models.TextChoices):
        BOOKED = 'забронирован', 'Забронирован'
        PAID = 'оплачен', 'Оплачен'
        CANCELLED = 'отменён', 'Отменён'

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Мероприятие"
    )

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Участник"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BOOKED,
        verbose_name="Статус"
    )

    number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Номер билета"
    )

    objects = TicketManager()

    def __str__(self):
        return f"{self.number} - {self.participant.name}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ['number']
