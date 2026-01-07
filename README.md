# Remind_project
**Project Overview**
The core objective of this project is to create "Smart Chatbots" that do more than just answer questions; they actively help the user remember information by generating conceptual quizzes based on past interactions.

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
