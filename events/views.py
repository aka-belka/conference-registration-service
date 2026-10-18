import sqlite3
from django.shortcuts import render

DB_PATH = "data/conference.sqlite"


def events(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    events = conn.execute("""
        SELECT
            id,
            title,
            date,
            max_seats,
            registered
        FROM events
        ORDER BY date;
    """).fetchall()
    conn.close()
    return render(request, "events/event_list.html", {"events": events})


def tickets(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    tickets = conn.execute("""
        SELECT
            tickets.number AS ticket_number,
            tickets.status AS ticket_status,
            events.title AS event_title,
            participants.name AS participant_name
        FROM tickets
        JOIN events
        ON tickets.event_id = events.id
        JOIN participants
        ON tickets.participant_id = participants.id;
    """).fetchall()
    conn.close()
    return render(request, "events/tickets.html", {"tickets": tickets})


def event_detail(request, event_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    event = conn.execute("""
        SELECT
            id,
            title,
            date,
            max_seats,
            registered
        FROM events
        WHERE id = ?;
    """, [event_id]).fetchone()
    conn.close()
    return render(request, "events/event_detail.html", {"event": event})


def search_events(request):
    search_date = request.GET.get("date")
    events = []
    if search_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        events = conn.execute("""
            SELECT
                id,
                title,
                date,
                max_seats,
                registered
            FROM events
            WHERE date = ?
        """, [search_date]).fetchall()
        conn.close()
    return render(request, "events/search.html", {"events": events, "search_date": search_date})


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    statistics_data = conn.execute("""
        SELECT
            events.title AS event_title,
            COUNT(tickets.id) AS tickets_count
        FROM events
        LEFT JOIN tickets ON events.id = tickets.event_id
        GROUP BY events.id, events.title
        ORDER BY tickets_count DESC;
    """).fetchall()
    conn.close()
    return render(request, "events/statistics.html", {"statistics": statistics_data})
