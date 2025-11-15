from django.urls import path
from ..views import (
    manage_organizer_profile,
    manage_organizer_events,
    manage_organizer_event,
)

urlpatterns = [
    # Organizer profile management
    path('profile/', manage_organizer_profile, name='manage_organizer_profile'),
    
    # Organizer events management
    path( "events/", manage_organizer_events, name="manage_organizer_events"),
    path( "events/<int:event_id>/", manage_organizer_event, name="manage_organizer_event"),
]