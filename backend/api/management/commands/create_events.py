from decimal import Decimal
from datetime import timedelta
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from api.models import Event, Organizer, Category  # <-- adjust if needed
from api.utils import moderate_event_content       # <-- adjust if needed


class Command(BaseCommand):
    help = "Create a bunch of events for organizer 'organizer666', including images from URLs."

    def handle(self, *args, **options):
        try:
            organizer = Organizer.objects.get(username="organizer666")
        except Organizer.DoesNotExist:
            raise CommandError("Organizer with username 'organizer666' does not exist.")

        categories = list(Category.objects.all())
        if not categories:
            raise CommandError("No Category objects found. Create some categories first.")

        sample_events = [
            {
                "title": "Tech Conference 2025",
                "description": "A full-day conference on the latest in web and AI.",
                "price": Decimal("99.99"),
                "days_from_now": 7,
                "image_url": "https://picsum.photos/seed/tech_conference_2025/1200/800",
                "image_name": "tech_conference_2025.jpg",
            },
            {
                "title": "Local Music Night",
                "description": "Live performances from local bands and artists.",
                "price": Decimal("15.00"),
                "days_from_now": 14,
                "image_url": "https://picsum.photos/seed/local_music_night/1200/800",
                "image_name": "local_music_night.jpg",
            },
            {
                "title": "Startup Pitch Evening",
                "description": "Pitch your startup idea to a panel of investors.",
                "price": Decimal("0.00"),
                "days_from_now": 21,
                "image_url": "https://picsum.photos/seed/startup_pitch_evening/1200/800",
                "image_name": "startup_pitch_evening.jpg",
            },
            {
                "title": "Art & Wine Workshop",
                "description": "Guided painting session with wine tasting.",
                "price": Decimal("45.00"),
                "days_from_now": 10,
                "image_url": "https://picsum.photos/seed/art_wine_workshop/1200/800",
                "image_name": "art_wine_workshop.jpg",
            },
            {
                "title": "Yoga in the Park",
                "description": "Outdoor yoga session suitable for all levels.",
                "price": Decimal("10.00"),
                "days_from_now": 3,
                "image_url": "https://picsum.photos/seed/yoga_in_the_park/1200/800",
                "image_name": "yoga_in_the_park.jpg",
            },
        ]

        created_count = 0

        for data in sample_events:
            title = data["title"]
            description = data["description"]
            price = data["price"]
            date = timezone.now() + timedelta(days=data["days_from_now"])
            image_url = data["image_url"]
            image_name = data["image_name"]

            moderation_result = moderate_event_content(title=title, description=description)
            if not moderation_result["approved"]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped '{title}' — rejected by moderation: {moderation_result['reason']}"
                    )
                )
                continue

            event = Event.objects.create(
                organizer=organizer,
                title=title,
                description=description,
                price=price,
                date=date,
                approved=True,
                moderation_notes=moderation_result["reason"],
            )

            # Download and attach image via urllib
            try:
                with urlopen(image_url, timeout=10) as resp:
                    image_data = resp.read()
            except (HTTPError, URLError, TimeoutError) as e:
                self.stdout.write(
                    self.style.WARNING(f"Failed to fetch image for '{title}' from {image_url}: {e}")
                )
            else:
                event.picture.save(
                    image_name,
                    ContentFile(image_data),
                    save=True,
                )

            event.category.set(categories[:2])
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created event: {event.title} (id={event.id})"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created_count} events for organizer666."))