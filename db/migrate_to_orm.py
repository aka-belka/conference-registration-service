import os
import sqlite3
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conference.settings')
django.setup()

from participants.models import Participant  # noqa: E402
from events.models import Event, Ticket  # noqa: E402

OLD_DB = "data/conference.sqlite"


def migrate():
    conn = sqlite3.connect(OLD_DB)
    conn.row_factory = sqlite3.Row

    # Участники
    for row in conn.execute("SELECT * FROM participants"):
        Participant.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'email': row['email'],
            }
        )

    # Мероприятия
    for row in conn.execute("SELECT * FROM events"):
        Event.objects.update_or_create(
            id=row['id'],
            defaults={
                'title': row['title'],
                'date': row['date'],
                'max_seats': row['max_seats'],
                'registered': row['registered'],
            }
        )

    # Билеты
    for row in conn.execute("SELECT * FROM tickets"):
        Ticket.objects.update_or_create(
            id=row['id'],
            defaults={
                'event_id': row['event_id'],
                'participant_id': row['participant_id'],
                'status': row['status'],
                'number': row['number'],
            }
        )

    conn.close()
    print("Данные перенесены.")


if __name__ == "__main__":
    migrate()
