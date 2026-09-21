def add_participant(participants: list[dict], name: str, email: str) -> dict:
    participant_id = len(participants) + 1
    participant = {
        "id": participant_id,
        "name": name,
        "email": email,
    }
    participants.append(participant)
    return participant


def find_participant_by_email(participants: list[dict], email: str) -> dict | None:
    for participant in participants:
        if participant["email"].lower() == email.lower():
            return participant
    return None


def find_participants_by_name(participants: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [p for p in participants if query_lower in p["name"].lower()]


def sort_participants_by_name(participants: list[dict]) -> list[dict]:
    return sorted(participants, key=lambda p: p["name"].lower())


def show_participants(participants: list[dict]) -> None:
    if not participants:
        print("Список участников пуст.")
        return
    print(f"{'ID':<5}{'Имя':<25}{'Email':<30}")
    print("-" * 60)
    for participant in participants:
        print(f"{participant['id']:<5}{participant['name']:<25}{participant['email']:<30}")
