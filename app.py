from datetime import date
import pandas as pd
import streamlit as st
import db
import services
import pharmacy
import triage

db.init_db()
pharmacy.init_pharmacy()
st.set_page_config(page_title="MediConnect (demo)", page_icon="🏥")
st.title("🏥 MediConnect (demo)")
st.caption("Demo only: sample data, not a real medical service.")
st.header("Not sure which doctor?")
symptoms = st.text_area("Describe your symptoms in a few words")
if st.button("Suggest a specialist"):
    if not symptoms.strip():
        st.warning("Please describe your symptoms first.")
    else:
        result = triage.suggest_specialty(symptoms)
        if result["emergency"]:
            st.error(result["reason"])
            if result["specialty"]:
                st.info(f"After you've been seen, a follow-up with a {result['specialty']} may help.")
        else:
            st.success(f"Suggested: {result['specialty']}. {result['reason']}")
        st.caption(triage.DISCLAIMER)
area = st.selectbox("Your area", list(services.AREAS))
user_lat, user_lon = services.AREAS[area]

st.header("Find a doctor")
specialty = st.selectbox("Specialty", ["All"] + services.list_specialties())
name_query = st.text_input("Search by doctor name")
doctors = services.sort_by_distance(services.search_doctors(specialty, name_query), user_lat, user_lon)
if doctors:
    st.dataframe(pd.DataFrame(doctors)[["name", "specialty", "city", "distance_km"]], hide_index=True)
else:
    st.header("Book an appointment")
    st.info("No doctors match your search.")
if doctors:
    doctor = st.selectbox("Doctor", doctors, format_func=lambda d: f"{d['name']} ({d['specialty']})")
    day = st.date_input("Date", min_value=date.today())
    taken = services.booked_times(doctor["id"], str(day))
    free = [t for t in services.SLOTS if t not in taken]
    if free:
        slot = st.selectbox("Time", free)
        patient = st.text_input("Your name")
        if st.button("Book"):
            ok, msg = services.book_appointment(doctor["id"], patient, str(day), slot)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    else:
        st.warning("No free slots on this date.")
else:
    st.info("No doctors found.")

st.header("My appointments")
lookup = st.text_input("Enter the name you booked with", key="lookup_name")
if lookup.strip():
    mine = services.get_appointments(lookup)
    if mine:
        for a in mine:
            c1, c2 = st.columns([4, 1])
            c1.write(f"{a['date']} {a['time']}: {a['doctor']} ({a['specialty']})")
            if c2.button("Cancel", key=f"cancel{a['id']}"):
                services.cancel_appointment(a["id"], lookup)
                st.rerun()
    else:
        st.info("No appointments found for that name.")

st.header("Nearby pharmacies")
nearby = services.sort_by_distance(pharmacy.list_pharmacies(), user_lat, user_lon)
st.dataframe(pd.DataFrame(nearby)[["name", "city", "distance_km"]], hide_index=True)

st.header("Map")
doctor_pts = pd.DataFrame(doctors, columns=["lat", "lon"])
pharmacy_pts = pd.DataFrame(pharmacy.list_pharmacies())[["lat", "lon"]]
st.caption("Doctors and pharmacies shown on the map (demo locations).")
st.map(pd.concat([doctor_pts, pharmacy_pts]))