from rest_framework import serializers
from ..models import Event
from ..utils import(
    GetCategoriesMixin,
    GetEventsMixin
)


class GetCategoriesSerializer(GetCategoriesMixin, serializers.Serializer):
    """
    Public: Returns all categories.
    """
    def to_representation(self, validated_data):
        return {
            "categories": self.get_categories_public()
        }


class GetEventsSerializer(GetEventsMixin, serializers.Serializer):
    """
    Public: List all approved events.
    """
    def to_representation(self, validated_data):
        return {"events": self.get_public_events()}


class GetEventSerializer(GetEventsMixin, serializers.Serializer):
    """
    Public: Get details for a single approved event.
    """
    def validate(self, attrs):
        event_id = self.context.get("event_id")
        try:
            event = Event.objects.get(id=event_id, approved=True)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found.")
        attrs["event"] = event
        return attrs

    def to_representation(self, validated_data):
        return {"event": self._event_to_dict(validated_data["event"])}

