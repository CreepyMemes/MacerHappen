from django.urls import path
from ..views import (
    get_organizers_public,
    get_organizer_profile_public,
    get_participant_profile_public,
)

urlpatterns = [
    path('organizers/', get_organizers_public, name='get_organizers_list'),
    path('organizers/<int:organizer_id>/profile/', get_organizer_profile_public, name='get_organizer_profile_public'),
    path('participants/<int:participant_id>/profile/', get_participant_profile_public, name='get_participant_profile_public'),
]
