import sqlite3
from django.shortcuts import render

DB_PATH = "data/conference.sqlite"


def participants(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    participants_list = conn.execute("""
        SELECT
            id,
            name,
            email
        FROM participants
        ORDER BY name;
    """).fetchall()
    conn.close()
    return render(request, "participants/participant_list.html", {"participants": participants_list})


def participant_detail(request, participant_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    participant = conn.execute("""
        SELECT
            id,
            name,
            email
        FROM participants
        WHERE id = ?;
    """, [participant_id]).fetchone()
    conn.close()
    return render(request, "participants/participant_detail.html", {"participant": participant})
