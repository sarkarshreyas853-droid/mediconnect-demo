import json
import os

from dotenv import load_dotenv
from groq import Groq

import services

load_dotenv()

MODEL = "openai/gpt-oss-120b"
DISCLAIMER = (
    "This is not a diagnosis. It only suggests which type of doctor to see. "
    "In an emergency, call 112 (India) or go to the nearest hospital."
)
EMERGENCY_WORDS = [
    "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
    "severe bleeding", "unconscious", "stroke", "seizure", "overdose", "suicide",
]


def is_emergency(text):
    t = text.lower()
    return any(w in t for w in EMERGENCY_WORDS)


def suggest_specialty(symptoms):
    """Returns {"emergency": bool, "specialty": str or None, "reason": str}."""
    if is_emergency(symptoms):
        return {
            "emergency": True,
            "specialty": "Cardiologist" if "chest" in symptoms.lower() else None,
            "reason": "These symptoms may be serious. Please seek emergency care now.",
        }

    allowed = services.list_specialties()
    prompt = (
        "You help a patient choose WHICH TYPE of doctor to see. You never diagnose.\n"
        f"Allowed specialties: {allowed}\n"
        f"Patient says: {symptoms}\n"
        'Reply with only JSON like {"specialty": "<one allowed specialty>", "reason": "<one short sentence>"}. '
        "If unsure, choose General Physician."
    )
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = resp.choices[0].message.content
        data = json.loads(text[text.find("{"): text.rfind("}") + 1])
        specialty = data.get("specialty")
        reason = data.get("reason", "")
    except Exception:
        specialty, reason = "General Physician", "Could not reach the AI service, so a general physician is suggested."

    if specialty not in allowed:
        specialty = "General Physician"
    return {"emergency": False, "specialty": specialty, "reason": reason}