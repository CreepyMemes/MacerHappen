from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, UniqueConstraint, Avg, Sum
from django.db import models
from enum import Enum

class Roles(Enum):
    """
    User role definitions: Admin, Participant, Organizer.
    """
    ADMIN = 'ADMIN'
    ORGANIZER = 'ORGANIZER'
    PARTICIPANT = 'PARTICIPANT'

    @classmethod
    def choices(cls):
        return [(role.value, role.name) for role in cls]
    

class UserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        
        if not username:
            raise ValueError('Username is required')
        
        role = extra_fields.get('role', Roles.CLIENT.value)

        if role != Roles.ADMIN.value and not email:
            raise ValueError('Email is required for non-admin users')

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        if not username:
            raise ValueError('Superuser must have a username')
        
        if extra_fields.get('role') != Roles.ADMIN.value:
            raise ValueError('Superuser must have role=ADMIN')
        
        admin = Admin(username=username, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin


class User(AbstractUser):
    """
    Custom user model using our custom manager.
    """
    def _get_profile_image_path(instance, filename):
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import get_image_path
        return get_image_path(instance, filename, 'profile')
    
    def _username_validator():
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import username_validator
        return username_validator
    
    username = models.CharField(validators=[_username_validator()], max_length=150, unique=True)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices(), default=Roles.PARTICIPANT.value)
    profile_image = models.ImageField(upload_to=_get_profile_image_path, null=True, blank=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['email'],
                condition=~Q(role=Roles.ADMIN.value),  # only enforce uniqueness for non-admins
                name='unique_email_non_admin'
            )
        ]
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'is_active': self.is_active,
            'date_joined': self.date_joined.strftime('%Y-%m-%d') if self.date_joined else None,
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image.url if self.profile_image else None,
        }


class Admin(User):
    """
    Admins are created by the system using the `createsuperuser` command.
    They are granted full permissions (staff and superuser) and do not require an email.
    """
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.ADMIN.value

        self.is_staff = True
        self.is_superuser = True

        super().save(*args, **kwargs)


    def to_dict(self):
        base = super().to_dict()
        # base.update({
        #     'total_participants': self.total_participants,
        #     'total_organizers': self.total_organizers,
        #     'total_appointments': self.total_appointments,
        #     'completed_appointments': self.completed_appointments,
        #     'cancelled_appointments': self.cancelled_appointments,
        #     'ongoing_appointments': self.ongoing_appointments,
        #     'total_revenue': self.total_revenue,
        #     'total_reviews': self.total_reviews,
        #     'average_rating': self.average_rating,
        # })
        return base


class Participant(User):
    """
    Participants are regular users who can register themselves via the API.
    They must provide a valid email and username during registration.
    """
    def _phone_number_validator():
        """
        Methohd that imports here to avoid circular import issues.
        """
        from ..utils import phone_number_validator
        return phone_number_validator
    
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[_phone_number_validator()], max_length=16, blank=True, null=True)

    categories = models.ManyToManyField("Category", related_name="participants", blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=999999)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.PARTICIPANT.value

        if not self.email:
            raise ValueError('Participant must have an email')
        
        super().save(*args, **kwargs)

    def to_dict(self):
        base = super().to_dict()
        base.update({      
            'name': self.name,
            'surname': self.surname,
            'phone_number': self.phone_number,
            'categories': [category.to_dict() for category in self.categories.all()],
            'budget': float(self.budget),
        })
        return base


class Organizer(User):
    """
    Organizers are regular users who can register themselves via the API.
    They must provide a valid email and username during registration.
    """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = Roles.ORGANIZER.value

        if not self.email:
            raise ValueError('Organizer must have an email')
        
        super().save(*args, **kwargs)
    
    # @property
    # def total_revenue(self):
    #     from .appointment import AppointmentStatus
    #     """
    #     Returns the sum of the services in all completed appointments for this organizer.
    #     """
    #     revenue = (
    #         self.appointments_received.filter(status=AppointmentStatus.COMPLETED.value)
    #         .annotate(price_sum=Sum('services__price'))
    #         .aggregate(total=Sum('price_sum'))['total']
    #     )
    #     return float(revenue) if revenue else 0.0
    
    
    def to_dict(self):
        """
        Returns a JSON-serializable dict representation of the review.
        """
        base = super().to_dict()
        base.update({
            'name': self.name,
            'surname': self.surname,
            'description': self.description,
            # 'total_revenue': self.total_revenue,
        })
        return base