from db import get_conn

PHARMACIES = [
    ("Sample Pharmacy A", "Kolkata", 22.5750, 88.3700),
    ("Sample Pharmacy B", "Kolkata", 22.5400, 88.3500),
    ("Sample Pharmacy C", "Kolkata", 22.6000, 88.3000),
]


def init_pharmacy():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM pharmacies").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO pharmacies (name, city, lat, lon) VALUES (?, ?, ?, ?)", PHARMACIES
        )
    conn.commit()
    conn.close()


def list_pharmacies():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM pharmacies").fetchall()
    conn.close()
    return [dict(r) for r in rows]