"""
Medical Chatbot - Student Project
----------------------------------
Educational medical assistant with safety guardrails.
Not a replacement for professional medical advice.
"""

import os
import streamlit as st
from openai import OpenAI


# -------------------------
# Configuration
# -------------------------

st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺",
    layout="centered"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMERGENCY_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "can't breathe",
    "suicidal",
    "unconscious",
    "stroke",
    "seizure",
    "severe bleeding",
]


SYSTEM_PROMPT = """
You are a medical informational assistant.

Strict Rules:
- You are NOT a doctor.
- Do NOT provide diagnosis.
- Provide educational information only.
- Always recommend consulting a healthcare professional.
- If symptoms are serious, recommend urgent care.

Structure response exactly as:

Possible Causes:
Red Flags:
Home Care Advice:
When to See a Doctor:
"""


# -------------------------
# Safety Layer
# -------------------------

def detect_emergency(message: str) -> bool:
    """Detect possible emergency symptoms."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)


def generate_medical_response(age: int, gender: str, symptoms: str) -> str:
    """Call OpenAI API safely."""

    user_context = f"""
    Patient Age: {age}
    Patient Gender: {gender}
    Symptoms: {symptoms}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_context}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


# -------------------------
# UI
# -------------------------

st.title("🩺 AI Medical Chatbot")
st.warning("⚠️ This chatbot is for educational purposes only. It is NOT medical advice.")

age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Patient Gender", ["Select", "Male", "Female", "Other"])
symptoms = st.text_area("Describe your symptoms")

if st.button("Get Medical Guidance"):

    if not symptoms:
        st.error("Please describe symptoms.")
    elif detect_emergency(symptoms):
        st.error("🚨 This may be a medical emergency. Please seek immediate medical care.")
    else:
        with st.spinner("Analyzing symptoms..."):
            try:
                response = generate_medical_response(age, gender, symptoms)
                st.success("Here is the medical guidance:")
                st.markdown(response)
            except Exception as exc:
                st.error(f"Error: {exc}")