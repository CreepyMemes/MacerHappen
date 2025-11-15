from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordValidationMixin:
    """
    Utility mixin to handle common password validation checks
    """
    def validate_password(self, value):
        validate_password(value)
        return value
    

class EmailValidationMixin:
    """
    Utility mixin to handle common email validation checks
    """
    def validate_email_unique(self, attrs, user_instance=None):
        from ..models import User

        email = attrs['email']
        user = User.objects.filter(email=email)

        if user_instance:
            user = user.exclude(pk=user_instance.pk)

        if user.exists():
            raise serializers.ValidationError(f'The email "{email}" is already taken.')
        
        attrs['email'] = email
        return attrs


class UsernameValidationMixin:
    """
    Utility mixin to handle common username validation checks
    """
    def validate_username_unique(self, attrs, user_instance=None): 
        from ..models import User

        username = attrs['username']
        user = User.objects.filter(username=username)

        if user_instance:
            user = user.exclude(pk=user_instance.pk)
        
        if user.exists():
            raise serializers.ValidationError(f'The username "{username}" is already taken.')
        
        attrs['username'] = username
        return attrs

    def validate_username_format(self, attrs):
        from ..utils import username_validator

        username = attrs['username']

        try:
            username_validator(username)
        except:
            raise serializers.ValidationError("Username can only contain ASCII letters, digits, and underscores")
        
        return attrs


class PhoneNumberValidationMixin:
    """
    Utility mixin to handle phone number validation checks
    """
    def validate_phone_number_format(self, attrs):
        from ..utils import phone_number_validator

        phone_number = attrs.get("phone_number")

        if phone_number:
            try:
                phone_number_validator(phone_number)
            except:
                raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed (E.164 format).")
        
        return attrs
    

class UIDTokenValidationSerializer(serializers.Serializer):
    """
    Utility serializer that handlles token checks, from which other serializers inherit
    """
    def validate_uid_token(self, attrs, target_key='user'):
        from .utils import get_user_from_uid_token

        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        if not uidb64 or not token:
            raise serializers.ValidationError("Missing uid or token.")

        user = get_user_from_uid_token(uidb64, token)

        attrs[target_key] = user
        return attrs


class ModelInstanceOrIDValidationMixin:
    """
    Mixin to fetch and validate a user model instance from either an instance or a PK in context.
    """
    def validate_user_model(self, model, attrs, check_active):
        from ..models import User
        model_name = model.__name__
        out_key = model_name.lower()
        context_keys = [out_key, f"{out_key}_id"]
        found = None
        
        # Get value for the first key found
        for key in context_keys:
            if key in self.context:
                found = self.context[key]
                break

        # If not found in `context` search in `attrs`
        for key in context_keys:
            if key in attrs:
                found = attrs[key]
                break
            
        if not found:
            raise serializers.ValidationError(f"No {model_name} or ID provided in context.")
        
        # If it's the correct model instance, return directly
        if isinstance(found, model):
            if check_active and not found.is_active:
                raise serializers.ValidationError(f"{model_name} is inactive.")
            
            attrs[out_key] = found
            return attrs
        
        # If instance of User, get the correct related model (participant/organizer/admin):
        if isinstance(found, User):
            user_type_name = model_name.lower()

            if hasattr(found, user_type_name):
                user_type = getattr(found, user_type_name, None)

                if user_type:
                    if check_active and not user_type.is_active:
                        raise serializers.ValidationError(f"{model_name} is inactive.")
                    
                    attrs[out_key] = user_type
                    return attrs
                
            raise serializers.ValidationError(f"User does not have a {user_type_name} profile.")

        # If it's a valid integer pk, query for instance
        if isinstance(found, int):
            try:
                user = model.objects.get(pk=found, is_active=True)
            except model.DoesNotExist:
                raise serializers.ValidationError(f'{model_name} with ID: "{found}" does not exist or is inactive.')
            
            attrs[out_key] = user
            return attrs

        # If it's neither, fallback error
        raise serializers.ValidationError(f"{model_name} must be provided as an instance or a primary key, not '{found}'.")


class UserValidationMixin(ModelInstanceOrIDValidationMixin):
    """
    Mixin to validate that a user_id from context exists and is active. Also adds 'user' to attrs.
    """
    def validate_user(self, attrs, check_active=True):
        from ..models import User
        return self.validate_user_model(User, attrs, check_active)


class AdminValidationMixin(ModelInstanceOrIDValidationMixin):
    """
    Mixin to validate that an Admin instance or ID from context, ensure active, adds 'admin' to attrs.
    """
    def validate_admin(self, attrs, check_active=True):
        from ..models import Admin
        return self.validate_user_model(Admin, attrs, check_active)
    

class ParticipantValidationMixin(ModelInstanceOrIDValidationMixin):
    """
    Mixin to validate that a Participant instance or ID from context, ensure active, adds 'participant' to attrs.
    """
    def validate_participant(self, attrs, check_active=True):
        from ..models import Participant
        return self.validate_user_model(Participant, attrs, check_active)


class OrganizerValidationMixin(ModelInstanceOrIDValidationMixin):
    """
    Mixin to validate that a Organizer instance or ID from context, ensure active, adds 'organizer' to attrs.
    """
    def validate_organizer(self, attrs, check_active=True):
        from ..models import Organizer
        return self.validate_user_model(Organizer, attrs, check_active)


class CategoryValidationMixin:
    """
    Provides helpers to validate category IDs.
    """
    def validate_categories(self, attrs, field_name="category_ids"):
        from ..models import Category

        ids = attrs.get(field_name, [])
        if not ids:
            return attrs
        
        categories = Category.objects.filter(id__in=ids)

        if categories.count() != len(ids):
            raise serializers.ValidationError("One or more categories IDs are invalid.")
        
        attrs["categories"] = categories
        return attrs


class EventValidationMixin:
    """
    Helpers to find and validate events.
    """
    def validate_find_event(self, attrs):
        from ..models import Event

        organizer = attrs["organizer"]
        event_id = self.context.get("event_id")

        try:
            event = Event.objects.get(id=event_id, organizer=organizer)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found for this organizer.")
        
        attrs["event"] = event
        return attrs


class SwipeValidationMixin:
    """
    Helpers for swipe creation/update.
    """
    def validate_event_for_swipe(self, attrs):
        from ..models import Event
        participant = attrs["participant"]
        event_id = attrs.get("event_id")

        if not event_id:
            raise serializers.ValidationError("event_id is required.")
        
        try:
            event = Event.objects.get(id=event_id, approved=True)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found or not approved.")

        attrs["event"] = event
        return attrs
    
class GetCategoriesMixin:
    def get_categories_public(self):
        from ..models import Category
        return [{"id": c.id, "name": c.name} for c in Category.objects.all()]


class GetEventsMixin:
    """
    Helpers to serialize events.
    """
    def get_events_for_organizer(self, organizer_id):
        from ..models import Event

        events = Event.objects.filter(organizer_id=organizer_id).order_by("-created_at")
        return [self._event_to_dict(e) for e in events]

    def get_public_events(self):
        from ..models import Event
        
        events = Event.objects.filter(approved=True).order_by("date")
        return [self._event_to_dict(e) for e in events]

    def _event_to_dict(self, event):
        return {
            "id": event.id,
            "organizer_id": event.organizer_id,
            "title": event.title,
            "description": event.description,
            "price": float(event.price),
            "date": event.date,
            "approved": event.approved,
            "categories": [c.id for c in event.category.all()],
        }