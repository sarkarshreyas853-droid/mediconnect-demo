# MediConnect (demo)

![tests](https://github.com/sarkarshreyas853-droid/mediconnect-demo/actions/workflows/tests.yml/badge.svg)

A demo healthcare web app: find doctors and pharmacies on a map, book appointments, and get an AI suggestion for which type of specialist to see.

> **Demo only.** All doctors, pharmacies and locations are made-up sample data. It is not a real medical service, takes no payments, sells no medicine and gives no medical advice.

## Features
- **Find a doctor:** filter sample doctors by specialty or search by name, sorted by distance from your chosen area.
- **Book an appointment:** pick a date and time; taken slots are hidden, and the database also rejects double-bookings.
- **My appointments:** look up bookings by name and cancel them, which frees the slot.
- **Nearby pharmacies and map:** sample doctors and pharmacies shown on a map, sorted by distance.
- **Symptom-to-specialist helper:** an LLM (Groq) suggests a type of doctor from a description of symptoms. It only chooses from the specialties in the database, never diagnoses, and always shows a disclaimer.
- **Emergency safeguard:** symptoms such as "chest pain" skip the AI and show an emergency message instead.

## Tech
Python, Streamlit, SQLite, pandas, Groq API, pytest, GitHub Actions.

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `db.py` | SQLite connection and doctor/appointment tables with sample doctors |
| `services.py` | Search, booking, cancellation and distance logic |
| `pharmacy.py` | Sample pharmacy directory |
| `triage.py` | Symptom-to-specialist helper and emergency check |
| `test_mediconnect.py` | pytest test suite |
| `.github/workflows/tests.yml` | Runs the tests on every push |

## Run locally
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file containing your own key (never commit this file):
```
GROQ_API_KEY=your_key_here
```
Then start the app:
```
streamlit run app.py
```
Without a key, everything works except the symptom helper, which falls back to suggesting a general physician.

## Tests
```
pytest -v
```
21 tests cover booking, double-booking prevention, cancellation permissions, input validation, doctor search, distance sorting and emergency detection. Each test uses its own temporary database. Tests run automatically on every push with GitHub Actions.

## Limitations
- Sample data only; no real doctors, pharmacies or users.
- No login or accounts.
- Appointments are looked up by name only, so anyone who knows a name could cancel its bookings.
- The emergency check is a simple keyword list, not a clinical tool.
- The AI suggestion can be wrong and is not medical advice.

## Author
Shreyas Sarkar