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


class GetAdminsMixin:
    """
    Mixin for retrieving and serializing Admin models.
    """
    def get_admins_queryset(self):
        """
        Returns Admin queryset in the system.
        """
        from ..models import Admin
        return Admin.objects.all()
    
    def get_admin_private(self, admin):
        """
        Returns all data for a single admin.
        """
        return admin.to_dict()
    
    def get_admins_private(self):
        """
        Returns all admins as full dicts.
        """
        return [self.get_admin_private(a) for a in self.get_admins_queryset()]
    

class GetParticipantsMixin:
    """
    Mixin for retrieving and serializing Participant models.
    """
    _PUBLIC_EXCLUDES = ['email', 'phone_number', 'is_active', 'total_appointments', 'completed_appointments', 'next_appointment', 'total_spent']

    def get_participants_queryset(self, show_all=False):
        """
        Returns Participant queryset in the system.
        If show_all is True, returns all participants.
        """
        from ..models import Participant
        return Participant.objects.filter(is_active=True) if not show_all else Participant.objects.all()
    
    def get_participant_public(self, participant):
        """
        Returns only the public data for a single participant.
        """
        data = participant.to_dict().copy()
        for field in self._PUBLIC_EXCLUDES:
            data.pop(field, None)
        return data
    
    def get_participant_private(self, participant):
        """
        Returns all data for a single participant.
        """
        return participant.to_dict()
    
    def get_participants_private(self, show_all=False):
        """
        Returns all participants as full dicts (all or only active).
        """
        return [self.get_participant_private(b) for b in self.get_participants_queryset(show_all=show_all)]
    
    def get_participants_public(self):
        """
        Returns all active participants as public dicts.
        """
        return [self.get_participant_public(b) for b in self.get_participants_queryset()]


class GetOrganizersMixin:
    """
    Mixin for retrieving and serializing Organizer models.
    """
    _PUBLIC_EXCLUDES = ['email', '',  '', '', 'is_active', '']

    def get_organizers_queryset(self, show_all=False):
        """
        Returns Organizer queryset in the system.
        If show_all is True, returns all organizers.
        """
        from ..models import Organizer
        return Organizer.objects.filter(is_active=True) if not show_all else Organizer.objects.all()
    
    def get_organizer_public(self, barber):
        """
        Returns only the public data for a single organizer.
        """
        data = organizer.to_dict().copy()
        for field in self._PUBLIC_EXCLUDES:
            data.pop(field, None)
        return data
    
    def get_organizer_private(self, organizer):
        """
        Returns all data for a single organizer.
        """
        return organizer.to_dict()
    
    def get_organizers_private(self, show_all=False):
        """
        Returns all organizers as full dicts (all or only active).
        """
        return [self.get_organizer_private(b) for b in self.get_organizers_queryset(show_all=show_all)]
    
    def get_organizers_public(self):
        """
        Returns all active organizers as public dicts.
        """
        return [self.get_organizer_public(b) for b in self.get_organizers_queryset()]
    
    def get_organizers_completed_public(self, participant):
        """
        Returns public data for all organizers that the participant had a completed appointment with.
        """
        from ..models import Organizer
        from ..models import AppointmentStatus

        # All ids of organizers the participant had a completed appointment with
        organizer_ids = participant.appointments_created.filter(status=AppointmentStatus.COMPLETED.value).values_list('organizer_id', flat=True).distinct()

        # Only active organizers (is_active=True), matching get_organizers_public
        return [self.get_organizer_public(organizer) for organizer in Organizer.objects.filter(id__in=organizer_ids, is_active=True)]
