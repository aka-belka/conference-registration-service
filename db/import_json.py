import json
from db.database import get_connection

EVENTS_FILE = "data/events.json"
PARTICIPANTS_FILE = "data/participants.json"
TICKETS_FILE = "data/tickets.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_events(conn):
    events = load_json(EVENTS_FILE)
    conn.executemany(
        """
    INSERT INTO events (
    id,
    title,
    date,
    max_seats,
    registered
    )
    VALUES (?, ?, ?, ?, ?)
    """,
        [
            (
                event["id"],
                event["title"],
                event["date"],
                event["max_seats"],
                event["registered"],
            )
            for event in events
        ],
    )


def import_participants(conn):
    participants = load_json(PARTICIPANTS_FILE)
    conn.executemany(
        """
    INSERT INTO participants (
    id,
    name,
    email
    )
    VALUES (?, ?, ?)
    """,
        [
            (
                participant["id"],
                participant["name"],
                participant["email"],
            )
            for participant in participants
        ],
    )


def import_tickets(conn):
    tickets = load_json(TICKETS_FILE)
    conn.executemany(
        """
    INSERT INTO tickets (
    id,
    event_id,
    participant_id,
    status,
    number
    )
    VALUES (?, ?, ?, ?, ?)
    """,
        [
            (
                ticket["id"],
                ticket["event_id"],
                ticket["participant_id"],
                ticket["status"],
                ticket["number"],
            )
            for ticket in tickets
        ],
    )


def main():
    conn = get_connection()
    try:
        import_events(conn)
        import_participants(conn)
        import_tickets(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
