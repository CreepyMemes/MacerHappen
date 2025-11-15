from django.db import models
from .user import Organizer
from .category import Category

class Event(models.Model):
    """
    Event model representing an event created by an organizer.
    """
    def _get_event_image_path(instance, filename):
        """
        Method that imports here to avoid circular import issues.
        """
        from ..utils import get_image_path
        return get_image_path(instance, filename, 'event')
    
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name="events")

    picture = models.ImageField(upload_to=_get_event_image_path, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name="events")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    # AI moderation: only approved events appear in feed
    approved = models.BooleanField(default=False)
    moderation_notes = models.TextField(blank=True, null=True)  # why approved/rejected
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
