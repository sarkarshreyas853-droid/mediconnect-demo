import math
import sqlite3
from db import get_conn

SLOTS = ["09:00", "10:00", "11:00", "12:00", "15:00", "16:00", "17:00"]


def list_specialties():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT specialty FROM doctors ORDER BY specialty").fetchall()
    conn.close()
    return [r["specialty"] for r in rows]


def search_doctors(specialty=None, name_query=""):
    sql = "SELECT * FROM doctors WHERE 1=1"
    params = []
    if specialty and specialty != "All":
        sql += " AND specialty = ?"
        params.append(specialty)
    if name_query.strip():
        sql += " AND LOWER(name) LIKE ?"
        params.append(f"%{name_query.strip().lower()}%")
    conn = get_conn()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def booked_times(doctor_id, date):
    conn = get_conn()
    rows = conn.execute(
        "SELECT time FROM appointments WHERE doctor_id = ? AND date = ?", (doctor_id, date)
    ).fetchall()
    conn.close()
    return [r["time"] for r in rows]


def book_appointment(doctor_id, patient_name, date, time):
    if not patient_name.strip():
        return False, "Please enter your name."
    if time not in SLOTS:
        return False, "Invalid time slot."
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO appointments (doctor_id, patient_name, date, time) VALUES (?, ?, ?, ?)",
            (doctor_id, patient_name.strip(), date, time),
        )
        conn.commit()
        return True, "Appointment booked."
    except sqlite3.IntegrityError:
        return False, "That slot is already taken."
    finally:
        conn.close()
def get_appointments(patient_name):
    conn = get_conn()
    rows = conn.execute(
        "SELECT a.id, d.name AS doctor, d.specialty, a.date, a.time "
        "FROM appointments a JOIN doctors d ON d.id = a.doctor_id "
        "WHERE LOWER(a.patient_name) = LOWER(?) ORDER BY a.date, a.time",
        (patient_name.strip(),),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def cancel_appointment(appointment_id, patient_name):
    conn = get_conn()
    cur = conn.execute(
        "DELETE FROM appointments WHERE id = ? AND LOWER(patient_name) = LOWER(?)",
        (appointment_id, patient_name.strip()),
    )
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if deleted:
        return True, "Appointment cancelled."
    return False, "No matching appointment found."
AREAS = {
    "Park Street": (22.5535, 88.3520),
    "Salt Lake": (22.5867, 88.4171),
    "Howrah": (22.5839, 88.3426),
    "Behala": (22.4986, 88.3103),
    "Dum Dum": (22.6203, 88.3980),
}


def distance_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def sort_by_distance(items, lat, lon):
    out = []
    for item in items:
        d = dict(item)
        d["distance_km"] = round(distance_km(lat, lon, d["lat"], d["lon"]), 1)
        out.append(d)
    return sorted(out, key=lambda x: x["distance_km"])