class Participant:
    def __init__(self, participant_id: int, name: str, email: str) -> None:
        self.id = participant_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "Participant":
        return cls(
            participant_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


def add_participant(participants: list[Participant], name: str, email: str) -> Participant:
    participant_id = len(participants) + 1
    participant = Participant(participant_id, name, email)
    participants.append(participant)
    return participant


def find_participant_by_email(participants: list[Participant], email: str) -> Participant | None:
    for participant in participants:
        if participant.email.lower() == email.lower():
            return participant
    return None


def find_participants_by_name(participants: list[Participant], query: str) -> list[Participant]:
    query_lower = query.lower()
    return [p for p in participants if query_lower in p.name.lower()]


def sort_participants_by_name(participants: list[Participant]) -> list[Participant]:
    return sorted(participants, key=lambda p: p.name.lower())


def show_participants(participants: list[Participant]) -> None:
    if not participants:
        print("Список участников пуст.")
        return
    print(f"{'ID':<5}{'Имя':<25}{'Email':<30}")
    print("-" * 60)
    for p in participants:
        print(f"{p.id:<5}{p.name:<25}{p.email:<30}")
