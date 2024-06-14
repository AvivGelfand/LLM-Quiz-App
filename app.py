# app.py
import streamlit as st
from datetime import datetime
import json
from random import shuffle
from system_prompts import sys_prompt
from llm_operator import LLMOperator

# Check for API Key
if "GROQ_API_KEY" not in st.secrets:
    st.error("API key not found. Please add your API key to the Streamlit secrets.")
    st.stop()

# Initialize the LLMOperator
models = {
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}
llm_operator = LLMOperator(api_key=st.secrets["GROQ_API_KEY"], models=models, sys_prompt=sys_prompt)

# Streamlit app configuration
st.set_page_config(page_icon="💬", layout="wide", page_title="LLM Quiz Chat")

# Sidebar for conversation history
st.sidebar.title("Previous Conversations")
st.sidebar.write("Conversation history will appear here.")
conversation_history = st.sidebar.empty()
history = []

# Main UI
st.title("LLM-Powered Quiz Generator")

# Number of questions input
num_questions = st.selectbox("Number of quiz questions", options=range(1, 6), index=4)

# Select quiz topic
topic = st.selectbox("Select quiz topic", ["History","Computer Science" , "Business and Marketing Strategy"])

# Select difficulty level
difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])
# Add a progress bar
progress = st.progress(0)

# Initialize session state
if "questions" not in st.session_state:
    st.session_state["questions"] = None
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "answered" not in st.session_state:
    st.session_state["answered"] = 0


if st.button("🎉 Generate Quiz!"):
    with st.spinner("Generating quiz questions..."):
        try:
            questions = llm_operator.generate_questions_JSON(topic, difficulty, num_questions)
            if questions and "questions_list" in questions:
                st.session_state["questions"] = questions
                st.session_state.start_time = datetime.now()
                st.session_state.answered = 0
                for question in st.session_state["questions"]["questions_list"]:
                    shuffle(question["options"])  # Shuffle the options for each question
            else:
                st.error("Failed to generate questions. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if st.session_state["questions"]:
    questions = st.session_state["questions"]["questions_list"]
    for i, question in enumerate(questions):
        st.write(f"### Question {i+1}: {question['question']}")
        selected_options = [st.checkbox(option, key=f"{i}_{option}") for option in question["options"]]

        if st.button(f"Check Answer for Question {i+1}", key=f"check_{i}"):
            if any(selected_options):
                selected_answers = [option for option, selected in zip(question["options"], selected_options) if selected]
                if question["answer"] in selected_answers:
                    st.success(f"Correct! {question['answer_explanation']}")
                    st.session_state.answered += 1  # Increment counter only for correct answers
                else:
                    st.error(f"Incorrect! The correct answer is {question['answer']}. {question['answer_explanation']}")
            else:
                st.warning("Please select at least one option before checking the answer.")

        if st.session_state.answered == num_questions:
            st.balloons()
            total_time = datetime.now() - st.session_state.start_time
            st.write(f"🎉 Congratulations! You've completed the quiz in {total_time.seconds} seconds.")

# Run Streamlit with the following command
# myenv\Scripts\activate
# streamlit run app4.py
