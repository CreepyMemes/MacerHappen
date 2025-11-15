from rest_framework import serializers
from ..models import Swipe
from ..utils import (
    GetParticipantsMixin,
    ParticipantValidationMixin,
    CategoryValidationMixin,
    ParticipantValidationMixin, 
    SwipeValidationMixin, 
    GetEventsMixin,
    RecommendationMixin
)

class GetParticipantProfileSerializer(ParticipantValidationMixin, GetParticipantsMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given participant
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        participant = validated_data['participant']
        return {'profile': self.get_participant_private(participant)}


class DeleteParticipantProfileSerializer(ParticipantValidationMixin, serializers.Serializer):
    """
    Participant only: Deletes a given existing participant account.
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs

    def delete(self):
        self.validated_data['organizer'].delete()


class GetParticipantPreferencesSerializer(ParticipantValidationMixin, serializers.Serializer):
    """
    Participant only: Get current preferences (categories + budget).
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs

    def to_representation(self, validated_data):
        participant = validated_data["participant"]
        return {
            "categories": [c.id for c in participant.categories.all()],
            "budget": float(participant.budget),
        }


class UpdateParticipantPreferencesSerializer(ParticipantValidationMixin, CategoryValidationMixin, serializers.Serializer):
    """
    Participant only: Update preferences (categories + budget).
    """
    category_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        attrs = self.validate_participant(attrs)

        if not any(f in attrs for f in ("category_ids", "budget")):
            raise serializers.ValidationError("You must provide at least one of: categories or budget.")

        if "category_ids" in attrs:
            attrs = self.validate_categories(attrs, field_name="category_ids")

        return attrs

    def update(self, instance, validated_data):
        if "category_ids" in validated_data:
            instance.categories.set(validated_data["category_ids"])

        if "budget" in validated_data:
            instance.budget = validated_data["budget"]

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data["participant"], self.validated_data)
    

class CreateSwipeSerializer(ParticipantValidationMixin, SwipeValidationMixin, GetEventsMixin, serializers.Serializer):
    """
    Participant only: Create or update a swipe (like/dislike) on an event.
    """
    event_id = serializers.IntegerField(required=True)
    liked = serializers.BooleanField(required=True)

    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        attrs = self.validate_event_for_swipe(attrs)
        return attrs

    def create(self, validated_data):
        participant = validated_data["participant"]
        event = validated_data["event"]
        liked = validated_data["liked"]

        swipe, _ = Swipe.objects.update_or_create(
            participant=participant,
            event=event,
            defaults={"liked": liked},
        )
        return swipe


class GetSwipeHistorySerializer(ParticipantValidationMixin, serializers.Serializer):
    """
    Participant only: Get swipe history.
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs

    def to_representation(self, validated_data):
        participant = validated_data["participant"]
        swipes = Swipe.objects.filter(participant=participant).select_related("event")
        return {
            "swipes": [
                {
                    "event_id": s.event_id,
                    "liked": s.liked,
                    "created_at": s.created_at,
                }
                for s in swipes
            ]
        }
    

class GetRecommendationFeedSerializer(ParticipantValidationMixin, RecommendationMixin, serializers.Serializer):
    """
    Participant only: Get personalized event feed.
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs

    def to_representation(self, validated_data):
        participant = validated_data["participant"]
        events = self.get_recommendations(participant)
        return {"events": events}
    
