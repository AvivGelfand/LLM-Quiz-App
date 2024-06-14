# app.py

from typing import Generator, List, Dict
from groq import Groq


import streamlit as st
from llm_chat_operator import LLMOperator

# Initialize LLMOperator with your API key
api_key = 'your_api_key_here'
llm_operator = LLMOperator(api_key)

# Sidebar for conversation history
st.sidebar.title("Previous Conversations")
st.sidebar.write("Conversation history will appear here.")

conversation_history = st.sidebar.empty()
history = []

# Main UI
st.title("LLM-Powered Quiz Generator")

# Number of questions input
num_questions = st.slider("Number of quiz questions", min_value=1, max_value=8, value=5)

# Select quiz topic
topic = st.selectbox("Select quiz topic", ["Science", "History", "Geography"])

# Select difficulty level
difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])


# Generate questions button
if st.button("Generate Questions"):
    questions = llm_operator.generate_quiz_questions(num_questions, topic, difficulty)
    history.append({"topic": topic, "difficulty": difficulty, "questions": questions})
    conversation_history.write(history)

    # Display generated questions
    st.subheader("Generated Quiz Questions")
    for question in questions:
        st.write(question)

