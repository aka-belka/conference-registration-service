from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="events"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("search_events/", views.search_events, name="search_events"),
    path("statistics/", views.statistics, name="statistics"),
    path("tickets/", views.tickets, name="tickets"),
    path("tickets_paginated/", views.tickets_paginated, name="tickets_paginated"),
    path("tickets_active/", views.active_tickets, name="tickets_active"),
    path("tickets_by_event_status/", views.tickets_by_event_status, name="tickets_by_event_status"),
]
