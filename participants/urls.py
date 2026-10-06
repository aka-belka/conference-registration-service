from django.urls import path

from . import views

urlpatterns = [
    path("", views.participants, name="participants"),
    path("<int:participant_id>/", views.participant_detail, name="participant_detail"),
]
