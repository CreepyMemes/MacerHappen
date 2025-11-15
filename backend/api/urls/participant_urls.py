from django.urls import path
from ..views import (
    manage_participant_preferences,
    create_swipe,
    get_swipe_history,
)


urlpatterns = [
    # Participant profile management
    path('preferences/', manage_participant_preferences, name='manage_participant_preferences'),
    
    # Swipe actions
    path('swipes/', create_swipe, name='create_swipe'),
    path('swipes/history/', get_swipe_history, name='get_swipe_history'),
]