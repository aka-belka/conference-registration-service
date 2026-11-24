from django.contrib import admin
from django.db.models import Count, Q

from .models import Event, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ('number', 'participant', 'status')
    show_change_link = True


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'date',
        'max_seats',
        'registered_count',
    )

    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('date',)
    ordering = ('date',)
    list_per_page = 20

    inlines = [TicketInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(
            _registered_count=Count(
                'tickets',
                filter=~Q(
                    tickets__status=Ticket.Status.CANCELLED
                ),
            )
        )

    @admin.display(
        description='Зарегистрировано',
        ordering='_registered_count',
    )
    def registered_count(self, obj):
        return obj._registered_count


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'event',
        'participant',
        'status',
    )

    list_display_links = ('id',)
    search_fields = (
        'number',
        'event__title',
        'participant__name',
        'participant__email',
    )
    list_filter = ('status', 'event')
    ordering = ('number',)
    list_per_page = 20
    list_select_related = ('event', 'participant')


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
