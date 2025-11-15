from django.db import models
from .user import Participant
from .event import Event

class Swipe(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="swipes")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="swipes")

    liked = models.BooleanField()  # True = right swipe, False = left swipe
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("participant", "event")  # cannot swipe same event twice

    def __str__(self):
        return f"{self.participant.username} -> {self.event.title} ({'like' if self.liked else 'dislike'})"
