import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# Configure page and load API key [cite: 690]
st.set_page_config(page_title="Gemini Clone", layout="centered")
load_dotenv()

# Initialize Gemini Client [cite: 692]
client = genai.Client(api_key='AIzaSyDb7r7TodOoXMW1lRATO4h9DmLzRNarS9A')
MODEL_NAME = "gemini-2.0-flash-lite" 
DATA_FILE = "chat_history.json"

# Helper functions for local JSON storage [cite: 699, 724]
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"interactions": []}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"interactions": []}

def save_interaction(query, response):
    data = load_data()
    data["interactions"].append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat()
    })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# UI Header [cite: 741]
st.title("Gemini Clone with Local History")
st.caption("Check chat_history.json to see the background storage!")

# Initialize chat session state [cite: 747]
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat messages [cite: 750]
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Logic [cite: 758]
user_input = st.chat_input("Ask me anything...")
if user_input:
    # Add user message to session state [cite: 761]
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Gemini [cite: 769]
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[types.Content(role="user", parts=[types.Part.from_text(text=user_input)])]
    )
    
    # Display and save AI reply [cite: 790, 793]
    reply = response.text
    st.session_state.chat.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
    
    # Persistent storage [cite: 795]
    save_interaction(user_input, reply)