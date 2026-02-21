"""
Medical Chatbot - Student Project
----------------------------------
Educational medical assistant with safety guardrails.
Not a replacement for professional medical advice.
"""

import streamlit as st
import random

# -------------------------
# Configuration
# -------------------------

st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🩺",
    layout="centered"
)

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

# -------------------------
# Mock Response Generator (No API Key Needed!)
# -------------------------

def generate_mock_response(age: int, gender: str, symptoms: str) -> str:
    """Generate educational medical responses without using OpenAI API."""
    
    symptoms_lower = symptoms.lower()
    
    # Response templates based on symptom categories
    if "headache" in symptoms_lower:
        return """
**Possible Causes:**
- Tension headache from stress
- Dehydration
- Eye strain
- Migraine (if severe or with light sensitivity)

**Red Flags:**
- Worst headache of your life
- Headache after head injury
- With fever and stiff neck
- Sudden severe onset

**Home Care Advice:**
- Rest in a quiet, dark room
- Stay hydrated
- Apply cold or warm compress to forehead
- Over-the-counter pain relievers (follow package directions)

**When to See a Doctor:**
- If headache persists for more than 3 days
- If over-the-counter medications don't help
- For recurrent or severe headaches
"""

    elif "fever" in symptoms_lower or "cough" in symptoms_lower or "cold" in symptoms_lower:
        return """
**Possible Causes:**
- Common viral infection (like cold or flu)
- Upper respiratory infection
- Seasonal allergies (if no fever)

**Red Flags:**
- High fever over 103°F (39.4°C)
- Difficulty breathing
- Chest pain
- Confusion or disorientation

**Home Care Advice:**
- Rest and stay hydrated
- Use a humidifier for cough
- Warm tea with honey for sore throat
- Monitor temperature regularly

**When to See a Doctor:**
- Fever lasting more than 3 days
- Symptoms worsening after initial improvement
- Difficulty breathing develops
"""

    elif "stomach" in symptoms_lower or "nausea" in symptoms_lower or "vomit" in symptoms_lower:
        return """
**Possible Causes:**
- Food poisoning
- Viral gastroenteritis (stomach flu)
- Indigestion
- Stress or anxiety

**Red Flags:**
- Severe abdominal pain
- Blood in vomit or stool
- Signs of dehydration (no urination for 8+ hours)
- High fever with abdominal pain

**Home Care Advice:**
- Small sips of clear fluids
- BRAT diet (bananas, rice, applesauce, toast)
- Avoid dairy, caffeine, and fatty foods
- Rest your stomach

**When to See a Doctor:**
- If unable to keep fluids down for 24 hours
- Severe pain develops
- Symptoms persist beyond 3-4 days
"""

    elif "pain" in symptoms_lower and "back" in symptoms_lower:
        return """
**Possible Causes:**
- Muscle strain
- Poor posture
- Lifting injury
- Prolonged sitting

**Red Flags:**
- Loss of bladder/bowel control
- Numbness in legs or groin area
- Pain after a fall or injury
- With unexplained fever or weight loss

**Home Care Advice:**
- Alternate ice and heat therapy
- Gentle stretching (if not painful)
- Maintain good posture
- Use supportive chair or lumbar cushion

**When to See a Doctor:**
- Pain persists beyond 2 weeks
- Pain radiates down legs
- Weakness or numbness develops
"""

    else:
        # Generic response for other symptoms
        responses = [
            """
**Possible Causes:**
- Common viral illness
- Stress-related symptoms
- Minor infection or inflammation
- Could be related to lifestyle factors

**Red Flags:**
- Severe or worsening pain
- High fever
- Difficulty breathing
- Bleeding or unusual discharge

**Home Care Advice:**
- Rest and hydration are essential
- Monitor symptoms for changes
- Over-the-counter remedies as appropriate
- Maintain healthy diet and sleep

**When to See a Doctor:**
- If symptoms persist beyond 5-7 days
- If they significantly worsen
- For proper diagnosis and treatment
- Always trust your instincts about your health
""",
            """
**Based on the symptoms described:**

**Possible Causes:**
- Minor infection or inflammation
- Muscle tension or strain
- Environmental factors
- Stress response

**Red Flags to Watch For:**
- Worsening symptoms despite home care
- Development of new symptoms
- Interference with daily activities
- Signs of infection (redness, swelling, fever)

**Self-Care Recommendations:**
- Get adequate rest
- Stay well hydrated
- Maintain good nutrition
- Avoid known triggers

**Medical Consultation:**
- If no improvement in 3-5 days
- If symptoms become severe
- For persistent or recurrent issues
- For peace of mind and proper evaluation
"""
        ]
        return random.choice(responses)

# -------------------------
# Safety Layer
# -------------------------

def detect_emergency(message: str) -> bool:
    """Detect possible emergency symptoms."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)

# -------------------------
# UI
# -------------------------

st.title("🩺 AI Medical Chatbot")
st.warning("⚠️ This chatbot is for educational purposes only. It is NOT medical advice.")

# Simple disclaimer for mock mode
st.info("🔧 **Demo Mode**: Using sample responses (no API key required)")

age = st.number_input("Patient Age", min_value=0, max_value=120, step=1, value=30)
gender = st.selectbox("Patient Gender", ["Select", "Male", "Female", "Other"])
symptoms = st.text_area("Describe your symptoms", placeholder="e.g., headache, fever, cough...")

if st.button("Get Medical Guidance"):

    if not symptoms:
        st.error("Please describe your symptoms.")
    elif detect_emergency(symptoms):
        st.error("🚨 **This may be a medical emergency.** Please seek immediate medical care. Do not wait for online guidance.")
        st.markdown("""
        **Call emergency services (911 or local emergency number) immediately if:**
        - You're having difficulty breathing
        - You have chest pain or pressure
        - You're severely bleeding
        - Someone is unconscious
        """)
    else:
        with st.spinner("Analyzing symptoms..."):
            try:
                # Using mock response instead of OpenAI API
                response = generate_mock_response(age, gender, symptoms)
                st.success("📋 **Educational Medical Guidance:**")
                st.markdown(response)
                
                # Add footer disclaimer
                st.caption("---")
                st.caption("⚠️ **Remember**: This is educational information only. Always consult a healthcare professional for medical advice.")
            except Exception as exc:
                st.error(f"Error: {exc}")
