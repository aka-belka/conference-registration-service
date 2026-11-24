
from django import forms
from django.core.exceptions import ValidationError

from events.models import Event, Ticket
from participants.models import Participant


class TicketFilterForm(forms.Form):

    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=False,
        label="Мероприятие",
        empty_label="Все мероприятия",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    status = forms.ChoiceField(
        choices=[("", "Все статусы")] + list(Ticket.Status.choices),
        required=False,
        label="Статус",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    event_date = forms.DateField(
        required=False,
        label="Дата мероприятия",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            },
            format="%Y-%m-%d",
        ),
    )

    ordering = forms.ChoiceField(
        choices=[
            ("number", "Номер: по возрастанию"),
            ("-number", "Номер: по убыванию"),
            ("event__date", "Дата мероприятия: сначала ранние"),
            ("-event__date", "Дата мероприятия: сначала поздние"),
            ("participant__name", "Участник: А–Я"),
            ("-participant__name", "Участник: Я–А"),
        ],
        required=False,
        initial="number",
        label="Сортировка",
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["event", "participant", "number", "status"]

        labels = {
            "event": "Мероприятие",
            "participant": "Участник",
            "number": "Номер билета",
            "status": "Статус билета",
        }

        error_messages = {
            "number": {
                "unique": "Билет с таким номером уже существует. Укажите другой номер.",
            },
        }

        widgets = {
            "event": forms.Select(
                attrs={"class": "form-select"}
            ),
            "participant": forms.Select(
                attrs={"class": "form-select"}
            ),
            "number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, TICKET-001",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["event"].queryset = Event.objects.order_by("date", "title")
        self.fields["participant"].queryset = Participant.objects.order_by("name")

        if not self.instance.pk:
            self.fields["status"].choices = [
                choice
                for choice in self.fields["status"].choices
                if choice[0] != Ticket.Status.CANCELLED
            ]
        if self.instance and self.instance.pk:
            self.fields.pop("participant")

    def clean(self):
        cleaned_data = super().clean()

        event = cleaned_data.get("event")

        if self.instance.pk:
            participant = self.instance.participant
        else:
            participant = cleaned_data.get("participant")

        if not event or not participant:
            return cleaned_data

        status = cleaned_data.get("status")

        if status == Ticket.Status.CANCELLED:
            return cleaned_data

        duplicate_tickets = Ticket.objects.active().filter(
            event=event,
            participant=participant,
        )

        if self.instance.pk:
            duplicate_tickets = duplicate_tickets.exclude(
                pk=self.instance.pk
            )

        if duplicate_tickets.exists():
            raise ValidationError(
                "У этого участника уже есть активный билет "
                "на выбранное мероприятие."
            )

        active_tickets = Ticket.objects.active().filter(
            event=event
        )

        if self.instance.pk:
            active_tickets = active_tickets.exclude(
                pk=self.instance.pk
            )

        if active_tickets.count() >= event.max_seats:
            raise ValidationError(
                "На выбранное мероприятие больше нет свободных мест."
            )

        return cleaned_data
