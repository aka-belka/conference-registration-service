from django.contrib import admin

from events.models import Ticket
from .models import Participant


class TicketInline(admin.TabularInline):
    model = Ticket
    fk_name = 'participant'
    extra = 0
    fields = ('number', 'event', 'status')
    show_change_link = True


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('name',)
    search_fields = ('name', 'email')
    ordering = ('name',)
    list_per_page = 20

    inlines = [TicketInline]


admin.site.register(Participant, ParticipantAdmin)
