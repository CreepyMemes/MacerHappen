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
    help = "Create a bunch of Macerata-based events for organizer 'organizer666', including images from URLs (picsum.photos)."

    def handle(self, *args, **options):
        try:
            organizer = Organizer.objects.get(username="organizer666")
        except Organizer.DoesNotExist:
            raise CommandError("Organizer with username 'organizer666' does not exist.")

        categories = list(Category.objects.all())
        if not categories:
            raise CommandError("No Category objects found. Create some categories first.")

        # Tutti gli URL delle immagini usano picsum.photos con seed dedicato
        sample_events = [
            {
                "title": "Tech Meetup Macerata 2025",
                "description": "Incontro dedicato a sviluppatori, designer e startup di Macerata sulle ultime novità di web e AI.",
                "price": Decimal("19.99"),
                "days_from_now": 7,
                "image_url": "https://picsum.photos/seed/tech_meetup_macerata_2025/1200/800",
                "image_name": "tech_meetup_macerata_2025.jpg",
            },
            {
                "title": "Local Music Night in Piazza della Libertà",
                "description": "Serata di musica live con band locali sotto le luci del centro storico di Macerata.",
                "price": Decimal("12.00"),
                "days_from_now": 10,
                "image_url": "https://picsum.photos/seed/local_music_piazza_liberta/1200/800",
                "image_name": "local_music_piazza_liberta.jpg",
            },
            {
                "title": "Startup Pitch Evening Macerata",
                "description": "Presenta la tua idea di startup a un panel di mentor e investitori marchigiani.",
                "price": Decimal("0.00"),
                "days_from_now": 14,
                "image_url": "https://picsum.photos/seed/startup_pitch_macerata/1200/800",
                "image_name": "startup_pitch_macerata.jpg",
            },
            {
                "title": "Art & Wine Workshop a Palazzo Buonaccorsi",
                "description": "Laboratorio di pittura con degustazione di vini locali nel cuore di Macerata.",
                "price": Decimal("49.00"),
                "days_from_now": 18,
                "image_url": "https://picsum.photos/seed/art_wine_palazzo_buonaccorsi/1200/800",
                "image_name": "art_wine_palazzo_buonaccorsi.jpg",
            },
            {
                "title": "Yoga al Parco di Fontescodella",
                "description": "Sessione di yoga open-air adatta a tutti, tra il verde del Parco di Fontescodella.",
                "price": Decimal("8.00"),
                "days_from_now": 3,
                "image_url": "https://picsum.photos/seed/yoga_fontescodella/1200/800",
                "image_name": "yoga_fontescodella.jpg",
            },
            {
                "title": "Visita Guidata allo Sferisterio di Macerata",
                "description": "Tour guidato dello Sferisterio con racconti sulla storia dell’opera e dell’architettura maceratese.",
                "price": Decimal("15.00"),
                "days_from_now": 5,
                "image_url": "https://picsum.photos/seed/visita_guidata_sferisterio/1200/800",
                "image_name": "visita_guidata_sferisterio.jpg",
            },
            {
                "title": "Opera sotto le Stelle allo Sferisterio",
                "description": "Spettacolo lirico all’aperto nel celebre Sferisterio di Macerata.",
                "price": Decimal("65.00"),
                "days_from_now": 25,
                "image_url": "https://picsum.photos/seed/opera_sferisterio_sotto_le_stelle/1200/800",
                "image_name": "opera_sferisterio_sotto_le_stelle.jpg",
            },
            {
                "title": "Mercatino Artigianale in Piazza della Libertà",
                "description": "Esposizione di artigianato locale, prodotti tipici marchigiani e street food.",
                "price": Decimal("0.00"),
                "days_from_now": 2,
                "image_url": "https://picsum.photos/seed/mercatino_artigianale_piazza_liberta/1200/800",
                "image_name": "mercatino_artigianale_piazza_liberta.jpg",
            },
            {
                "title": "Degustazione di Vernaccia di Serrapetrona",
                "description": "Serata di degustazione di Vernaccia e altri vini del territorio maceratese.",
                "price": Decimal("25.00"),
                "days_from_now": 9,
                "image_url": "https://picsum.photos/seed/degustazione_vernaccia_macerata/1200/800",
                "image_name": "degustazione_vernaccia_macerata.jpg",
            },
            {
                "title": "Festival della Pizza Marchigiana",
                "description": "Forni a cielo aperto, pizza gourmet e musica dal vivo alle porte di Macerata.",
                "price": Decimal("5.00"),
                "days_from_now": 12,
                "image_url": "https://picsum.photos/seed/festival_pizza_marchigiana/1200/800",
                "image_name": "festival_pizza_marchigiana.jpg",
            },
            {
                "title": "Escursione tra le Colline Maceratesi",
                "description": "Trekking panoramico tra vigneti e uliveti con guida ambientale escursionistica.",
                "price": Decimal("20.00"),
                "days_from_now": 6,
                "image_url": "https://picsum.photos/seed/escursione_colline_maceratesi/1200/800",
                "image_name": "escursione_colline_maceratesi.jpg",
            },
            {
                "title": "Corso di Fotografia nel Centro Storico",
                "description": "Workshop per imparare a fotografare vicoli, piazze e scorci di Macerata.",
                "price": Decimal("35.00"),
                "days_from_now": 11,
                "image_url": "https://picsum.photos/seed/corso_fotografia_centro_storico_macerata/1200/800",
                "image_name": "corso_fotografia_centro_storico_macerata.jpg",
            },
            {
                "title": "Street Food Festival Macerata",
                "description": "Tre giorni di street food internazionale e specialità marchigiane.",
                "price": Decimal("3.00"),
                "days_from_now": 15,
                "image_url": "https://picsum.photos/seed/street_food_festival_macerata/1200/800",
                "image_name": "street_food_festival_macerata.jpg",
            },
            {
                "title": "Cinema all’Aperto allo Sferisterio",
                "description": "Proiezione di film d’autore all’aperto nello scenario unico dello Sferisterio.",
                "price": Decimal("9.50"),
                "days_from_now": 20,
                "image_url": "https://picsum.photos/seed/cinema_aperto_sferisterio/1200/800",
                "image_name": "cinema_aperto_sferisterio.jpg",
            },
            {
                "title": "Laboratorio di Cucina Tipica Marchigiana",
                "description": "Impara a preparare vincisgrassi, olive all’ascolana e altre ricette locali.",
                "price": Decimal("40.00"),
                "days_from_now": 8,
                "image_url": "https://picsum.photos/seed/laboratorio_cucina_marchigiana/1200/800",
                "image_name": "laboratorio_cucina_marchigiana.jpg",
            },
            {
                "title": "Mercato Contadino a Macerata",
                "description": "Prodotti freschi a km 0 dai produttori della provincia di Macerata.",
                "price": Decimal("0.00"),
                "days_from_now": 1,
                "image_url": "https://picsum.photos/seed/mercato_contadino_macerata/1200/800",
                "image_name": "mercato_contadino_macerata.jpg",
            },
            {
                "title": "Serata Jazz nel Cortile di Palazzo Buonaccorsi",
                "description": "Concerto jazz intimista nel cortile storico di Palazzo Buonaccorsi.",
                "price": Decimal("18.00"),
                "days_from_now": 13,
                "image_url": "https://picsum.photos/seed/serata_jazz_palazzo_buonaccorsi/1200/800",
                "image_name": "serata_jazz_palazzo_buonaccorsi.jpg",
            },
            {
                "title": "Workshop di Ceramica Artistica",
                "description": "Laboratorio pratico di ceramica ispirata alle tradizioni artigiane marchigiane.",
                "price": Decimal("30.00"),
                "days_from_now": 16,
                "image_url": "https://picsum.photos/seed/workshop_ceramica_artistica_macerata/1200/800",
                "image_name": "workshop_ceramica_artistica_macerata.jpg",
            },
            {
                "title": "Passeggiata Fotografica al Tramonto",
                "description": "Passeggiata serale per immortalare il tramonto sulle mura di Macerata.",
                "price": Decimal("14.00"),
                "days_from_now": 4,
                "image_url": "https://picsum.photos/seed/passeggiata_tramonto_macerata/1200/800",
                "image_name": "passeggiata_tramonto_macerata.jpg",
            },
            {
                "title": "Festival delle Birre Artigianali Maceratesi",
                "description": "Degustazione di birre artigianali locali, musica e street food.",
                "price": Decimal("22.00"),
                "days_from_now": 22,
                "image_url": "https://picsum.photos/seed/festival_birre_artigianali_macerata/1200/800",
                "image_name": "festival_birre_artigianali_macerata.jpg",
            },
            {
                "title": "Corso di Disegno Urbano a Macerata",
                "description": "Impara a disegnare scorci urbani e architetture storiche della città.",
                "price": Decimal("28.00"),
                "days_from_now": 19,
                "image_url": "https://picsum.photos/seed/corso_disegno_urbano_macerata/1200/800",
                "image_name": "corso_disegno_urbano_macerata.jpg",
            },
            {
                "title": "Notte Bianca di Macerata",
                "description": "Negozi aperti, concerti, spettacoli e dj set fino a tarda notte.",
                "price": Decimal("0.00"),
                "days_from_now": 30,
                "image_url": "https://picsum.photos/seed/notte_bianca_macerata/1200/800",
                "image_name": "notte_bianca_macerata.jpg",
            },
            {
                "title": "Fiera di San Giuliano",
                "description": "Tradizionale fiera cittadina con bancarelle, giostre e prodotti tipici.",
                "price": Decimal("0.00"),
                "days_from_now": 40,
                "image_url": "https://picsum.photos/seed/fiera_san_giuliano_macerata/1200/800",
                "image_name": "fiera_san_giuliano_macerata.jpg",
            },
            {
                "title": "Corso di Lingua e Cultura Marchigiana",
                "description": "Introduzione al dialetto e alle tradizioni popolari della provincia di Macerata.",
                "price": Decimal("60.00"),
                "days_from_now": 35,
                "image_url": "https://picsum.photos/seed/corso_cultura_marchigiana_macerata/1200/800",
                "image_name": "corso_cultura_marchigiana_macerata.jpg",
            },
            {
                "title": "Passeggiata Letteraria nel Centro Storico",
                "description": "Itinerario guidato tra luoghi legati a scrittori e poeti marchigiani.",
                "price": Decimal("10.00"),
                "days_from_now": 17,
                "image_url": "https://picsum.photos/seed/passeggiata_letteraria_macerata/1200/800",
                "image_name": "passeggiata_letteraria_macerata.jpg",
            },
            {
                "title": "Laboratorio di Street Art per Ragazzi",
                "description": "Workshop creativo di street art in uno spazio urbano autorizzato.",
                "price": Decimal("18.00"),
                "days_from_now": 21,
                "image_url": "https://picsum.photos/seed/laboratorio_street_art_macerata/1200/800",
                "image_name": "laboratorio_street_art_macerata.jpg",
            },
            {
                "title": "Festival del Libro a Macerata",
                "description": "Presentazioni, firmacopie e incontri con autori locali e nazionali.",
                "price": Decimal("0.00"),
                "days_from_now": 27,
                "image_url": "https://picsum.photos/seed/festival_libro_macerata/1200/800",
                "image_name": "festival_libro_macerata.jpg",
            },
            {
                "title": "Concerto di Musica Classica in Duomo",
                "description": "Ensemble d’archi e coro per una serata di grande musica nel Duomo di Macerata.",
                "price": Decimal("32.00"),
                "days_from_now": 24,
                "image_url": "https://picsum.photos/seed/concerto_classica_duomo_macerata/1200/800",
                "image_name": "concerto_classica_duomo_macerata.jpg",
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

            # Download and attach image via urllib (picsum.photos)
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

            # Associa le prime due categorie disponibili
            event.category.set(categories[:2])
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created event: {event.title} (id={event.id})"))

        self.stdout.write(self.style.SUCCESS(f"Done. Created {created_count} events for organizer666."))