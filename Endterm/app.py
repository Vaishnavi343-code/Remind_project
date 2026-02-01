import streamlit as st
import json
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai

# ------------------ ENV + CLIENT ------------------

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MEMORY_FILE = "memory.json"
REVIEW_FILE = "review.json"

# ------------------ JSON HELPERS ------------------

def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

memory = load_json(MEMORY_FILE, [])
reviews = load_json(REVIEW_FILE, [])

# ------------------ SPACED REPETITION ------------------

REVIEW_GAPS = {
    1: timedelta(days=1),
    2: timedelta(days=3),
    3: timedelta(days=7),
    4: timedelta(days=14)
}

def get_due_reviews():
    now = datetime.now()
    due = []
    for item in reviews:
        last = datetime.fromisoformat(item["last_reviewed"])
        if now - last >= REVIEW_GAPS[item["level"]]:
            due.append(item)
    return due

# ------------------ STREAMLIT UI ------------------

st.title("🤖 ReMind Agentic Tutor")

st.caption(
    "A Socratic chatbot with local memory and spaced repetition. "
    "It never answers directly and promotes active recall."
)

user_input = st.text_input("Ask something:")

# ------------------ MAIN CHAT LOGIC ------------------

if user_input:
    # store conversation memory
    memory.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().isoformat()
    })

    # store for spaced repetition
    reviews.append({
        "question": user_input,
        "level": 1,
        "last_reviewed": datetime.now().isoformat()
    })

    socratic_prompt = f"""
You are a Socratic tutor.
Rules:
- NEVER answer directly
- ALWAYS ask a guiding question
- Encourage the user to think
- Respond ONLY with questions

User query:
{user_input}
"""

    time.sleep(1)  # rate-limit safety

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=socratic_prompt
        )
        reply = response.text.strip()

    except Exception:
        # graceful fallback if API quota is exceeded
        reply = (
            "Let's think this through together. "
            "What do you already know about this topic, "
            "and which part feels confusing to you?"
        )

    memory.append({
        "role": "assistant",
        "content": reply,
        "time": datetime.now().isoformat()
    })

    save_json(MEMORY_FILE, memory)
    save_json(REVIEW_FILE, reviews)

    st.write("🤖:", reply)

# ------------------ REVIEW SECTION ------------------

st.subheader("📌 Concepts Due for Review")

due_items = get_due_reviews()

if not due_items:
    st.write("No reviews due yet 🎉")

for i, item in enumerate(due_items):
    # UNIQUE KEY FIX (prevents StreamlitDuplicateElementId)
    if st.button(
        item["question"],
        key=f"review_btn_{i}"
    ):
        item["level"] = min(item["level"] + 1, 4)
        item["last_reviewed"] = datetime.now().isoformat()
        save_json(REVIEW_FILE, reviews)
        st.success(f"Level increased → {item['level']}")
