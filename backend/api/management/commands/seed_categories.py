from django.core.management.base import BaseCommand
from api.models.category import Category  # adjust import based on your structure

DEFAULT_CATEGORIES = [
    "Music",
    "Tech",
    "Sports",
    "Food",
    "Nightlife",
    "Business",
    "Workshops",
    "Travel",
    "Art",
]

class Command(BaseCommand):
    help = "Seeds default event categories"

    def handle(self, *args, **kwargs):
        for name in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Categories seeded successfully!"))
