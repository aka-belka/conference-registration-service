from participants import (
    add_participant, find_participant_by_email,
    find_participants_by_name, sort_participants_by_name,
)


def test_add_participant():
    participants = []
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    assert len(participants) == 1
    assert participants[0]["name"] == "Бельская Валерия"
    assert participants[0]["id"] == 1


def test_find_participant_by_email():
    participants = []
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    add_participant(participants, "Берг Ксения", "berg_ks@mail.com")
    found = find_participant_by_email(participants, "SERGeevnau18@gmail.com")
    assert found is not None
    assert found["name"] == "Бельская Валерия"
    assert find_participant_by_email(participants, "akabelka@gmail.com") is None


def test_find_participants_by_name():
    participants = []
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    add_participant(participants, "Берг Ксения", "berg_ks@mail.com")
    add_participant(participants, "Халтаев Олег", "xalt2006@mail.com")
    found = find_participants_by_name(participants, "Валерия")
    assert len(found) == 1
    assert found[0]["name"] == "Бельская Валерия"


def test_sort_participants_by_name():
    participants = []
    add_participant(participants, "Берг Ксения", "berg_ks@mail.com")
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    add_participant(participants, "Халтаев Олег", "xalt2006@mail.com")
    sorted_list = sort_participants_by_name(participants)
    assert sorted_list[0]["name"] == "Бельская Валерия"
    assert sorted_list[1]["name"] == "Берг Ксения"
    assert sorted_list[2]["name"] == "Халтаев Олег"


def test_add_participant_increments_id():
    participants = []
    add_participant(participants, "Бельская Валерия", "sergeevnau18@gmail.com")
    add_participant(participants, "Берг Ксения", "berg_ks@mail.com")
    assert participants[0]["id"] == 1
    assert participants[1]["id"] == 2
