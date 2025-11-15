from rest_framework import serializers
from ..utils import (
    ParticipantValidationMixin,
    CategoryValidationMixin,
)
from ..models import Participant

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