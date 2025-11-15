from django.urls import path
from ..views import (
    manage_organizer_events,
    manage_organizer_event,
)

urlpatterns = [
    path( "events/", manage_organizer_events, name="manage_organizer_events"),
    path( "events/<int:event_id>/", manage_organizer_event, name="manage_organizer_event"),
]