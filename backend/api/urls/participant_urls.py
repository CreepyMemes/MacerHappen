from django.urls import path
from ..views import (
    manage_participant_preferences,
)


urlpatterns = [
    # Participant profile management
    path('preferences/', manage_participant_preferences, name='manage_participant_preferences'),
]