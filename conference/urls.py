from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls
from events import views as events_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("homepage.urls")),
    path("participants/", include("participants.urls")),
    path("events/", include("events.urls")),
    path("tickets/", events_views.tickets_paginated, name="tickets"),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
