import streamlit as st
import os
import json
from datetime import datetime, timedelta
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DATA_FILE = "chat_history.json" [cite: 804]

def load_data(): [cite: 808]
    if not os.path.exists(DATA_FILE): return {"interactions": []}
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_interaction(query, response): [cite: 837]
    data = load_data()
    data["interactions"].append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat() [cite: 846]
    })
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

st.title("RE-MIND: Time Bot")

if user_input := st.chat_input("Enter your query:"):
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=user_input)
    save_interaction(user_input, response.text)
    st.write(f"Assistant: {response.text}")

# Quiz Logic: Check for queries > 10 minutes old [cite: 1104]
st.sidebar.header("Retention Quizzes")
if st.sidebar.button("Check for Quizzes"):
    data = load_data()
    found_quiz = False
    
    for item in data["interactions"]:
        timestamp = datetime.fromisoformat(item["time"])
        if datetime.now() - timestamp >= timedelta(minutes=10): # 10-minute check [cite: 1104]
            st.sidebar.info(f"Quiz for query from {timestamp.strftime('%H:%M:%S')}")
            prompt = f"Ask a conceptual quiz question about: {item['query']}"
            quiz = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
            st.sidebar.write(quiz.text)
            found_quiz = True
            break # Quiz on one item at a time
    
    if not found_quiz:
        st.sidebar.write("No queries are older than 10 minutes yet.")