from django.contrib import admin

from .models import Event, Ticket


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'max_seats', 'registered')
    list_filter = ('date',)
    search_fields = ('title',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('number', 'event', 'participant', 'status')
    list_filter = ('status',)
    search_fields = ('number',)


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
