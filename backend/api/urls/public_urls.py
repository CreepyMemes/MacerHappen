from django.urls import path
from ..views import (
    get_events,
    get_event_detail,
    get_categories,
)

urlpatterns = [
    path("events/", get_events, name="list_events"),
    path("events/<int:event_id>/", get_event_detail, name="get_event_detail"),
    path("categories/", get_categories, name="get_categories"),
]
