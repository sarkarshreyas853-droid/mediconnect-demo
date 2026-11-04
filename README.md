# MediConnect (demo)

A demo healthcare web app: find doctors and pharmacies on a map, book appointments, and get an AI suggestion for which type of specialist to see.

> **Demo only.** All doctors, pharmacies and locations are made-up sample data. It is not a real medical service, takes no payments, sells no medicine and gives no medical advice.

## Features
- **Find a doctor:** filter sample doctors by specialty or search by name, sorted by distance from your chosen area.
- **Book an appointment:** pick a date and time; taken slots are hidden, and the database also rejects double-bookings.
- **My appointments:** look up bookings by name and cancel them, which frees the slot.
- **Nearby pharmacies and map:** sample doctors and pharmacies shown on a map, sorted by distance.
- **Symptom-to-specialist helper:** an LLM (Groq) suggests a type of doctor from a description of symptoms. It only chooses from the specialties in the database, never diagnoses, and always shows a disclaimer.
- **Emergency safeguard:** symptoms such as "chest pain" skip the AI and show an emergency message instead..

## Tech
Python, Streamlit, SQLite, pandas, Groq API, pytest.

## Run locally
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file containing `GROQ_API_KEY=your_key_here`, then:
```
streamlit run app.py
```

## Tests
```
pytest -v
```
11 tests cover booking, double-booking prevention, input validation, specialty search and emergency detection. Each test uses its own temporary database.

## Limitations
- Sample data only; no real doctors, pharmacies or users.
- No login or accounts.
- The emergency check is a simple keyword list, not a clinical tool.
- The AI suggestion can be wrong and is not medical advice.

## Author
Shreyas Sarkar
