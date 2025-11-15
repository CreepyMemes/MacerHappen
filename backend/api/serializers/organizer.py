from rest_framework import serializers
from ..utils import (
    OrganizerValidationMixin,
    EventValidationMixin,
    CategoryValidationMixin,
    GetEventsMixin,
)
from ..models import Event

class GetOrganizerEventsSerializer(OrganizerValidationMixin, GetEventsMixin, serializers.Serializer):
    """
    Organizer only: List all events created by this organizer.
    """
    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        return attrs

    def to_representation(self, validated_data):
        organizer = validated_data["organizer"]
        return {"events": self.get_events_for_organizer(organizer.id)}


class CreateOrganizerEventSerializer(OrganizerValidationMixin, CategoryValidationMixin, GetEventsMixin, serializers.Serializer):
    """
    Organizer only: Create a new event.
    """
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    date = serializers.DateTimeField(required=True)
    category_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        attrs = self.validate_categories(attrs, field_name="category_ids")
        return attrs

    def create(self, validated_data):
        from ..utils import moderate_event_content

        organizer = validated_data["organizer"]
        categories = validated_data["categories"]
        title = validated_data["title"]
        description = validated_data["description"]

        # Run AI moderation BEFORE creating
        moderation_result = moderate_event_content(title=title, description=description)

        if not moderation_result["approved"]:
            # surface this as a validation error (HTTP 400)
            raise serializers.ValidationError({
                "detail": f"Event rejected by moderation: {moderation_result['reason']}"
            })

        # Only create if approved
        event = Event.objects.create(
            organizer=organizer,
            title=title,
            description=description,
            price=validated_data["price"],
            date=validated_data["date"],
            approved=True,  # already moderated
            moderation_notes=moderation_result["reason"],
        )
        event.category.set(categories)
        return event


class GetOrganizerEventDetailSerializer(OrganizerValidationMixin, EventValidationMixin, GetEventsMixin, serializers.Serializer):
    """
    Organizer only: Get details of a single event.
    """
    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        attrs = self.validate_find_event(attrs)
        return attrs

    def to_representation(self, validated_data):
        event = validated_data["event"]
        return {"event": self._event_to_dict(event, include_moderation=True)}


class UpdateOrganizerEventSerializer(OrganizerValidationMixin, EventValidationMixin, CategoryValidationMixin, GetEventsMixin, serializers.Serializer):
    """
    Organizer only: Update an existing event.
    """
    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    date = serializers.DateTimeField(required=False)
    category_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        attrs = self.validate_find_event(attrs)

        if not any(f in attrs for f in ("title", "description", "price", "date", "category_ids")):
            raise serializers.ValidationError("You must provide at least one field: title, description, price, date, category_ids.")
        
        if "category_ids" in attrs:
            attrs = self.validate_category_ids(attrs, field_name="category_ids")
        return attrs

    def update(self, instance, validated_data):
        if "title" in validated_data:
            instance.title = validated_data["title"]
        if "description" in validated_data:
            instance.description = validated_data["description"]
        if "price" in validated_data:
            instance.price = validated_data["price"]
        if "date" in validated_data:
            instance.date = validated_data["date"]
        if "categories" in validated_data:
            instance.category.set(validated_data["categories"])

        instance.save()
        return instance

    def save(self, **kwargs):
        return self.update(self.validated_data["event"], self.validated_data)


class DeleteOrganizerEventSerializer(OrganizerValidationMixin, EventValidationMixin, serializers.Serializer):
    """
    Organizer only: Delete an existing event.
    """
    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        attrs = self.validate_find_event(attrs)
        return attrs

    def delete(self):
        self.validated_data["event"].delete()