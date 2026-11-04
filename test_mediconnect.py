import pytest

import db
import pharmacy
import services
import triage


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    """Every test gets its own empty database, so tests never touch real data."""
    monkeypatch.setattr(db, "DB", str(tmp_path / "test.db"))
    db.init_db()
    pharmacy.init_pharmacy()


def test_booking_succeeds():
    ok, msg = services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    assert ok
    assert "booked" in msg.lower()
def test_get_appointments_lists_only_that_patient():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    services.book_appointment(2, "Ben", "2030-01-01", "10:00")
    mine = services.get_appointments("asha")
    assert len(mine) == 1
    assert mine[0]["time"] == "09:00"


def test_cancel_frees_the_slot():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    appt = services.get_appointments("Asha")[0]
    ok, _ = services.cancel_appointment(appt["id"], "Asha")
    assert ok
    ok_again, _ = services.book_appointment(1, "Ben", "2030-01-01", "09:00")
    assert ok_again


def test_cannot_cancel_someone_elses_appointment():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    appt = services.get_appointments("Asha")[0]
    ok, _ = services.cancel_appointment(appt["id"], "Ben")
    assert not ok
    assert len(services.get_appointments("Asha")) == 1


def test_cancelling_twice_fails():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    appt = services.get_appointments("Asha")[0]
    services.cancel_appointment(appt["id"], "Asha")
    ok, _ = services.cancel_appointment(appt["id"], "Asha")
    assert not ok

def test_double_booking_is_blocked():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    ok, msg = services.book_appointment(1, "Ben", "2030-01-01", "09:00")
    assert not ok
    assert "already taken" in msg.lower()


def test_same_slot_with_different_doctor_is_allowed():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    ok, _ = services.book_appointment(2, "Ben", "2030-01-01", "09:00")
    assert ok


def test_same_slot_on_different_day_is_allowed():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    ok, _ = services.book_appointment(1, "Ben", "2030-01-02", "09:00")
    assert ok


def test_empty_name_is_rejected():
    ok, msg = services.book_appointment(1, "   ", "2030-01-01", "09:00")
    assert not ok
    assert "name" in msg.lower()


def test_invalid_time_slot_is_rejected():
    ok, msg = services.book_appointment(1, "Asha", "2030-01-01", "03:33")
    assert not ok
    assert "invalid" in msg.lower()


def test_booked_slot_disappears_from_availability():
    services.book_appointment(1, "Asha", "2030-01-01", "09:00")
    assert "09:00" in services.booked_times(1, "2030-01-01")
    assert services.booked_times(2, "2030-01-01") == []


def test_search_filters_by_specialty():
    results = services.search_doctors("Cardiologist")
    assert len(results) == 1
    assert results[0]["specialty"] == "Cardiologist"


def test_search_all_returns_every_doctor():
    assert len(services.search_doctors("All")) == 5


def test_emergency_words_are_detected():
    assert triage.is_emergency("I have chest pain")
    assert triage.is_emergency("CANNOT BREATHE properly")


def test_normal_symptoms_are_not_emergencies():
    assert not triage.is_emergency("itchy skin rash for a week")


def test_distance_known_value():
    # one degree of latitude is about 111 km
    assert 110 < services.distance_km(22.0, 88.0, 23.0, 88.0) < 112


def test_sort_by_distance_puts_nearest_first():
    items = [
        {"name": "far", "lat": 23.0, "lon": 88.0},
        {"name": "near", "lat": 22.01, "lon": 88.0},
    ]
    result = services.sort_by_distance(items, 22.0, 88.0)
    assert [r["name"] for r in result] == ["near", "far"]
def test_search_by_name_is_case_insensitive():
    results = services.search_doctors("All", "sample two")
    assert len(results) == 1
    assert results[0]["name"] == "Dr. Sample Two"


def test_search_by_name_and_specialty_combined():
    assert len(services.search_doctors("Cardiologist", "two")) == 1
    assert services.search_doctors("Dermatologist", "two") == []


def test_search_with_no_match_returns_empty_list():
    assert services.search_doctors("All", "zzz") == []
def test_distance_is_zero_for_same_point():
    assert services.distance_km(22.57, 88.36, 22.57, 88.36) == 0