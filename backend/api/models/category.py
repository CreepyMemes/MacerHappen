from django.db import models

class Category(models.Model):
    """
    Category model representing event categories.
    Must be hardcoded in the database before use.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
