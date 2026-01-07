import streamlit as st
import os
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash-lite" [cite: 803]

st.title("RE-MIND: Counter Bot")

# Initialize session state for counter and query storage [cite: 705, 856]
if "query_counter" not in st.session_state:
    st.session_state.query_counter = 0
if "temp_queries" not in st.session_state:
    st.session_state.temp_queries = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User interaction
if user_input := st.chat_input("Ask a question..."): [cite: 713]
    st.session_state.query_counter += 1
    st.session_state.temp_queries.append(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    response = client.models.generate_content(model=MODEL_NAME, contents=user_input) [cite: 664]
    reply = response.text
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Check for quiz trigger (every 5 queries) [cite: 1101]
    if st.session_state.query_counter >= 5:
        st.sidebar.warning("Quiz Time! You have reached 5 queries.")
        
        # Select random query from the last 5 [cite: 944, 1102]
        random_topic = random.choice(st.session_state.temp_queries)
        
        quiz_prompt = f"Create a short conceptual quiz question about: {random_topic}. Do not give the answer." [cite: 991, 992]
        quiz_res = client.models.generate_content(model=MODEL_NAME, contents=quiz_prompt)
        
        st.sidebar.subheader("Random Quiz")
        st.sidebar.write(quiz_res.text)
        
        # Reset counter and list [cite: 1101]
        st.session_state.query_counter = 0
        st.session_state.temp_queries = []