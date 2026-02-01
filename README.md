# Remind_project
**Project Overview**
The core objective of this project is to create "Smart Chatbots" that do more than just answer questions; they actively help the user remember information by generating conceptual quizzes based on past interactions.

**Final submission: **
# ReMind Agentic Tutor – Final Project Report

## 1. Introduction

Most students today use AI systems in a passive manner: they ask a question, receive a ready-made answer, skim it, and move on. While this feels efficient, it leads to very poor long-term retention. The learner does not struggle with the concept, does not recall prior knowledge, and does not actively engage with the material. As a result, learning remains shallow.

The goal of the **ReMind Agentic Tutor** project is to address this problem by designing an AI-based learning assistant that actively promotes understanding and retention. The project is inspired by concepts discussed in the reference material, especially:

* The **Socratic method** for guided learning
* **Active recall** and **spaced repetition** for long-term memory
* Agentic behavior, where the system takes initiative instead of being a passive responder

The final system is a Streamlit-based chatbot that asks guiding questions instead of directly answering, stores learning history locally, schedules concepts for revision using spaced repetition, and behaves robustly even when external APIs fail.

---

## 2. Objectives

The objectives of this project are:

1. To implement a **Socratic chatbot** that never answers directly unless explicitly instructed.
2. To store conversation history locally and reuse it as context.
3. To implement a **spaced repetition system** that tracks concepts, learning levels, and review timings.
4. To design an **agentic chatbot** by combining Socratic questioning, memory, and revision logic.
5. To ensure the system is robust, explainable, and suitable for real-world learning scenarios.

---

## 3. System Overview

The ReMind Agentic Tutor is implemented as a Python application using **Streamlit** for the user interface. It integrates with the **Google Gemini API** (via the google-genai SDK) for generating Socratic prompts. All learning data is stored locally using JSON files, ensuring transparency and persistence.

### 3.1 Folder Structure

```
project/
│
├── app.py        # Main application logic
├── memory.json   # Conversation history storage
├── review.json   # Spaced repetition data
├── .env          # API key configuration
└── venv/         # Python virtual environment
```

---

## 4. Technologies Used

* **Python** – Core programming language
* **Streamlit** – Web-based UI framework
* **Google Gemini API** – Language model for generating Socratic questions
* **JSON** – Lightweight local data storage
* **datetime module** – Time-based review scheduling
* **python-dotenv** – Secure environment variable handling

---

## 5. Problem 11.1 – Socratic Chatbot

### 5.1 Design

The Socratic chatbot is designed with a strict rule: it must never directly answer user questions. Instead, it responds only with guiding questions that encourage the learner to think and reflect.

This behavior is enforced through:

* A carefully constructed system prompt
* Controlled response generation
* No preloaded or fabricated conversation history

### 5.2 Implementation

When the user enters a query:

1. The query is stored in `memory.json`.
2. A Socratic prompt is generated and sent to the language model.
3. The model’s response (a guiding question) is shown to the user.
4. The response is also stored locally.

This ensures that learning remains active and reflective rather than passive.

---

## 6. Problem 11.2 – Spaced Repetition Bot

### 6.1 Concept

Spaced repetition is a proven learning technique where concepts are reviewed at increasing intervals based on the learner’s familiarity. In this project, each concept is assigned a **level**, and the next review time depends on this level.

### 6.2 Levels and Review Intervals

| Level | Review Interval |
| ----- | --------------- |
| 1     | 1 day           |
| 2     | 3 days          |
| 3     | 7 days          |
| 4     | 14 days         |

### 6.3 Implementation

Each user query is stored in `review.json` with:

* `question`
* `level`
* `last_reviewed`

When the app loads:

1. Current time is compared with `last_reviewed`.
2. If the interval has passed, the question appears under **Concepts Due for Review**.
3. Clicking the question increases its level and updates the timestamp.

This mechanism ensures systematic and adaptive revision.

---

## 7. Problem 11.3 – Agentic Chatbot

### 7.1 Agentic Behavior

An agentic system does not merely respond to inputs; it tracks state, takes initiative, and adapts behavior over time. The ReMind Agentic Tutor demonstrates agentic behavior through:

* Persistent memory across sessions
* Automatic identification of concepts due for revision
* Adaptive difficulty via level progression
* Proactive learning reinforcement

### 7.2 Integration of Features

Problem 11.3 combines:

* Socratic questioning (Problem 11.1)
* Spaced repetition (Problem 11.2)
* Robust error handling for API failures

This results in a complete learning assistant rather than a simple chatbot.

---

## 8. Error Handling and Robustness

The application includes graceful handling of external API failures such as quota exhaustion. If the Gemini API is unavailable:

* The application does not crash
* A fallback Socratic question is shown
* Learning interaction continues uninterrupted

This improves reliability and demonstrates good software engineering practice.

---

## 9. Testing and Validation

The system was tested using multiple functional and edge-case scenarios:

* Verification of Socratic-only responses
* Persistence of conversation history across restarts
* Correct creation and updating of review entries
* Time-based appearance of due review questions
* Level progression upon review
* Stable behavior under API quota errors

All tests produced the expected outcomes.

---

## 10. Conclusion

The ReMind Agentic Tutor successfully demonstrates how AI can be used to promote active learning rather than passive consumption. By combining the Socratic method, spaced repetition, and agentic behavior, the system encourages deeper understanding and long-term retention.

The project aligns closely with the ideas discussed in the reference material and serves as a strong foundation for future extensions such as adaptive difficulty, performance analytics, or multi-topic learning paths.

---

## 11. Future Enhancements

Possible future improvements include:

* Personalized review intervals based on performance
* Topic categorization and tagging
* Visualization of learning progress
* Multi-user support

---

**End of Report**

**Midterm :**

**Key Features**
**Persistent Storage:** Saves chat logs locally to chat_history.json for long-term tracking.

**Counter-Based Quizzing:** Automatically triggers a knowledge check every 5 queries.

**Retention Quizzes:** Analyzes timestamps to prompt users with questions on topics they discussed over 10 minutes ago.

**Multi-Model Support:** Utilizes gemini-2.0-flash-lite and gemini-2.5-flash-lite for efficient processing.

**File: Description**
app.py: A classic Gemini clone featuring local JSON history storage.
counterbot.py: The ""RE-MIND: Counter Bot"" which quizzes users after every 5 interactions.
timebot.py: The ""RE-MIND: Time Bot"" designed for long-term retention via time-delayed quizzes.
WIDS.env.txt: Environment configuration file containing the necessary API keys.

**Technical Implementation**
**1. Data Persistence**
The applications use a localized JSON-based storage system to ensure that user interactions are not lost when the session ends.

**Loading:** Checks for chat_history.json and handles potential decoding errors.

**Saving:** Appends new queries, responses, and ISO-formatted timestamps to the local file.

**2. Smart Quiz Logic**
Two distinct logic flows are used to challenge the user's memory:

**Frequency Logic:** In counterbot.py, a query_counter tracks the number of user inputs. Once it hits 5, a random topic is selected from the previous 5 queries to generate a quiz.

**Temporal Logic:** In timebot.py, the system calculates the timedelta between the current time and the query timestamp. If the gap exceeds 10 minutes, the bot identifies it as a "retention candidate".

**3. API Integration**
The projects utilize the google-genai SDK to communicate with Gemini models.

**Client Initialization:** Securely loads the API key from environment variables.

**Content Generation:** Sends user prompts or specific quiz instructions (e.g., "Do not give the answer") to the model.

**Setup and Usage**

**1.Environment:** Rename WIDS.env.txt to .env and ensure your GEMINI_API_KEY is correctly set.

**2.Dependencies:** Install the required libraries:

Bash : pip install streamlit google-genai python-dotenv

**3.Running the Apps:**

To run the Counter Bot: streamlit run counterbot.py

To run the Time Bot: streamlit run timebot.py
