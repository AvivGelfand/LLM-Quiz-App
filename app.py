# app.py
# activate environment with the command: .\groq_streamlit\Scripts\activate
# run with the command: streamlit run app.py
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
if "attempts" not in st.session_state:
    st.session_state["attempts"] = []

# Display previous attempts in the sidebar
for idx, attempt in enumerate(st.session_state["attempts"]):
    if st.sidebar.button(f"Attempt {idx + 1} - {attempt['score']} Correct"):
        st.write(f"### Attempt {idx + 1} - {attempt['score']} Correct")
        st.write(f"Time: {attempt['timestamp']}")
        for i, question in enumerate(attempt['questions']):
            st.write(f"#### Question {i + 1}: {question['question']}")
            st.write(f"Your answer: {', '.join(attempt['answers'][i])}")
            st.write(f"Correct answer: {question['answer']}")
            st.write(f"Explanation: {question['answer_explanation']}")

# Main UI
st.title("LLM-Powered Quiz Generator")

# Number of questions input
num_questions = st.selectbox("Number of quiz questions", options=range(1, 6), index=4)

# Select quiz topic
topic = st.selectbox("Select quiz topic", ["History", "Computer Science", "Business and Marketing Strategy"])

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
    selected_answers = []
    for i, question in enumerate(questions):
        st.write(f"### {i + 1}. {question['question']}")
        selected_options = [st.checkbox(option, key=f"{i}_{option}") for option in question["options"]]
        selected_answers.append(selected_options)
        
        # Check if more than one option is selected
        if sum(selected_options) > 1:
            st.warning(f"⚠️ Question {i + 1}: More than one option selected. Only one answer is allowed.")

    if st.button("✔️ Check All Answers"):
        correct_answers = 0
        user_answers = []
        for i, question in enumerate(questions):
            if sum(selected_answers[i]) > 1:
                st.error(f"❌ Question {i + 1}: Incorrect! More than one option was selected.")
                user_answers.append([opt for opt, sel in zip(question["options"], selected_answers[i]) if sel])
            elif any(selected_answers[i]):
                user_selected = [option for option, selected in zip(question["options"], selected_answers[i]) if selected]
                user_answers.append(user_selected)
                if question["answer"] in user_selected:
                    st.success(f"✅ Question {i + 1}: Correct! {question['answer_explanation']}")
                    correct_answers += 1
                else:
                    st.error(f"❌ Question {i + 1}: Incorrect! The correct answer is {question['answer']}. {question['answer_explanation']}")
            else:
                st.warning(f"⚠️ Question {i + 1}: No options selected.")
                user_answers.append([])

        total_time = datetime.now() - st.session_state.start_time
        st.write(f"🎉 You got {correct_answers} out of {num_questions} correct in {total_time.seconds} seconds. The result will be saved in the sidebar.")
        if correct_answers == num_questions:
            st.balloons()
        
        # Save the attempt
        attempt = {
            "questions": questions,
            "answers": user_answers,
            "score": correct_answers,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state["attempts"].append(attempt)
