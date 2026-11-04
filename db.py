import sqlite3

DB = "mediconnect.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        city TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        UNIQUE (doctor_id, date, time),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    );
    """)
    if c.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO doctors (name, specialty, city, lat, lon) VALUES (?, ?, ?, ?, ?)",
            [
                ("Dr. Sample One", "General Physician", "Kolkata", 22.5726, 88.3639),
                ("Dr. Sample Two", "Cardiologist", "Kolkata", 22.5448, 88.3426),
                ("Dr. Sample Three", "Dermatologist", "Kolkata", 22.5958, 88.2636),
                ("Dr. Sample Four", "Pediatrician", "Kolkata", 22.6203, 88.4040),
                ("Dr. Sample Five", "Orthopedic", "Kolkata", 22.5100, 88.3500),
            ],
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database ready")