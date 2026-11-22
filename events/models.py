from django.db import models
from participants.models import Participant


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    date = models.DateField(verbose_name="Дата")
    max_seats = models.IntegerField(verbose_name="Максимум мест")
    registered = models.IntegerField(default=0, verbose_name="Зарегистрировано")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('забронирован', 'Забронирован'),
        ('оплачен', 'Оплачен'),
        ('отменён', 'Отменён'),
    ]
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
        choices=STATUS_CHOICES,
        default='забронирован',
        verbose_name="Статус"
    )
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер билета")

    def __str__(self):
        return f"{self.number} - {self.participant.name}"

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
