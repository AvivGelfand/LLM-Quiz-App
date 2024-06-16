# app.py
# activate environment with the command: .\groq_streamlit\Scripts\activate
# run with the command: streamlit run app.py
import streamlit as st
from datetime import datetime
from random import shuffle
from prompts import sys_prompt
from llm_operator import GroqOperator

# Check for API Key
if "GROQ_API_KEY" not in st.secrets:
    st.error("API key not found. Please add your API key to the Streamlit secrets.")
    st.stop()

# Initialize the LLMOperator
llm_operator = GroqOperator(api_key=st.secrets["GROQ_API_KEY"], sys_prompt=sys_prompt)

# Streamlit app configuration
st.set_page_config(page_icon="🧙‍♂️", layout="wide", page_title="LLM Quiz Wizard")

# Initialize session state
if "attempts" not in st.session_state:
    st.session_state["attempts"] = []
if "questions" not in st.session_state:
    st.session_state["questions"] = None
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "answered" not in st.session_state:
    st.session_state["answered"] = 0

# Sidebar for conversation history
st.sidebar.title("Previous Quiz Attempts")

def display_previous_attempts():
    for idx, attempt in enumerate(st.session_state["attempts"]):
        if st.sidebar.button(f"Attempt {idx + 1} : {attempt['score']}/{attempt['num_questions']} Correct"):
            st.write(f"### Attempt {idx + 1} - {attempt['score']}/{attempt['num_questions']} Correct")
            st.write(f"Time: {attempt['timestamp']}")
            for i, question in enumerate(attempt['questions']):
                st.write(f"### Question {i + 1}: {question['question']}")
                st.write(f"**Your answer**: {', '.join(attempt['answers'][i])}")
                st.write(f"**Correct answer**: {question['answer']}")
                st.write(f"**Explanation**: {question['answer_explanation']}")

def generate_quiz(topic, difficulty, num_questions):
    with st.spinner("Generating quiz questions..."):
        try:
            questions = llm_operator.generate_questions_JSON(topic, difficulty, num_questions)
            if questions and "questions_list" in questions:
                st.session_state["questions"] = questions
                st.session_state["start_time"] = datetime.now()
                st.session_state["answered"] = 0
                for question in st.session_state["questions"]["questions_list"]:
                    shuffle(question["options"])  # Shuffle the options for each question
            else:
                st.error("Failed to generate questions. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def display_generated_questions():
    st.markdown("## Generated Questions")
    questions = st.session_state["questions"]["questions_list"]
    selected_answers = []
    for i, question in enumerate(questions):
        st.write(f"### {i + 1}. {question['question']}")
        selected_options = [st.checkbox(option, key=f"{i}_{option}") for option in question["options"]]
        selected_answers.append(selected_options)
        
        if sum(selected_options) > 1:
            st.warning(f"⚠️ More than one option selected. Only one answer is allowed.")
    
    if st.button("✔️ Check All Answers"):
        check_answers(questions, selected_answers)

def check_answers(questions, selected_answers):
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
    
    total_time = datetime.now() - st.session_state["start_time"]
    st.write(f"🎉 You got {correct_answers} out of {num_questions} correct in {total_time.seconds} seconds. The result will be saved in the sidebar.\n")
    st.write(f"You can now generate a new quiz and challenge yourself again!")

    if correct_answers == num_questions:
        st.balloons()
    
    attempt = {
        "questions": questions,
        "num_questions": num_questions,
        "answers": user_answers,
        "score": correct_answers,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["attempts"].append(attempt)

# Main UI
st.title("LLM-Powered Quiz Generator")

topics = {
    "World History": ["Significant Inventions", "Ancient Civilizations", "Medieval History", "Modern History", "World Wars", "General"],
    "Marketing / Business Strategy": ["Brand Management", "Consumer Behavior", "Digital Marketing", "Market Research", "Strategic Planning", "General"],
    "Computer Science": ["Algorithms", "Data Structures", "Machine Learning", "Software Development", "General"],
    "Movies": ["Action Movies", "Comedy Movies", "Drama Movies", "Fantasy Movies", "Horror Movies", "General"],
    "Geography": ["Mountains", "Rivers", "Cities", "Deserts", "Oceans", "General"]
}

general_topic = st.selectbox("Select a quiz topic", list(topics.keys()))
sub_topic = st.selectbox("Select a quiz sub-topic", topics[general_topic])
topic = general_topic if sub_topic == "General" else sub_topic
difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])
num_questions = st.selectbox("Number of quiz questions", options=range(1, 11), index=4)

if st.button("🎉 Generate Quiz!"):
    generate_quiz(topic, difficulty, num_questions)

st.markdown("---")

if st.session_state["questions"]:
    display_generated_questions()
    st.markdown("---")

display_previous_attempts()
