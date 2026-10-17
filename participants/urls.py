from django.urls import path

from . import views

app_name = "participants"

urlpatterns = [
    path("", views.participants, name="participants"),
    path("<int:participant_id>/", views.participant_detail, name="participant_detail"),
]
