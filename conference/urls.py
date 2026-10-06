"""
URL configuration for conference project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from events import views as events_views

handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("homepage.urls")),
    path("participants/", include("participants.urls")),
    path("events/", include("events.urls")),
    path("tickets/", events_views.tickets, name="tickets"),
]
