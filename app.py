# app.py
# activate environment with the command: .\groq_streamlit\Scripts\activate
# run with the command: streamlit run app.py
import streamlit as st
from datetime import datetime
from random import shuffle
from system_prompts import sys_prompt
from groq_llm_operator import GroqLLMOperator

# Check for API Key
if "GROQ_API_KEY" not in st.secrets:
    st.error("API key not found. Please add your API key to the Streamlit secrets.")
    st.stop()



# Initialize the LLMOperator
models = {
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

llm_operator = GroqLLMOperator(api_key=st.secrets["GROQ_API_KEY"], models=models, sys_prompt=sys_prompt)

# Streamlit app configuration
st.set_page_config(page_icon="🧙‍♂️", layout="wide", page_title="LLM Quiz Wizard🪄")

# Sidebar for conversation history
st.sidebar.title("Previous Quiz Attempts")
if "attempts" not in st.session_state:
    st.session_state["attempts"] = []



# Main UI
st.title("LLM-Powered Quiz Generator")

# Number of questions input
num_questions = st.selectbox("Number of quiz questions", options=range(1, 11), index=4)

# Select quiz topic
topic = st.selectbox("Select quiz topic", ["Marketing / Business Strategy", "History", "Computer Science"])

# Select difficulty level
difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])

# # optional bonus feature: adding a progress bar
# progress = st.progress(1)

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
st.markdown("---")

if st.session_state["questions"]:
    st.markdown("## Generated Questions")

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
        """
        The following part checks the answers selected by the user and provides feedback.
        It also calculates the total score and the time taken to complete the quiz.
        """
        correct_answers = 0
        user_answers = []
        
        for i, question in enumerate(questions): # Iterate over each question

            # Check if more than one option is selected
            if sum(selected_answers[i]) > 1:
                st.error(f"❌ Question {i + 1}: Incorrect! More than one option was selected.")
                user_answers.append([opt for opt, sel in zip(question["options"], selected_answers[i]) if sel])
            # Check if any option is selected
            elif any(selected_answers[i]):
                user_selected = [option for option, selected in zip(question["options"], selected_answers[i]) if selected]
                user_answers.append(user_selected)
                # Check if the selected option is correct
                if question["answer"] in user_selected:
                    st.success(f"✅ Question {i + 1}: Correct! {question['answer_explanation']}")
                    correct_answers += 1
                else:
                    st.error(f"❌ Question {i + 1}: Incorrect! The correct answer is {question['answer']}. {question['answer_explanation']}")
            else:
                st.warning(f"⚠️ Question {i + 1}: No options selected.")
                user_answers.append([])

        # Calculate the total time taken to complete the quiz
        total_time = datetime.now() - st.session_state.start_time
        st.write(f"🎉 You got {correct_answers} out of {num_questions} correct in {total_time.seconds} seconds. The result will be saved in the sidebar.\n")

        # Show a balloon if all answers are correct
        if correct_answers == num_questions:
            st.balloons()
        
        # Save the attempt details in the session state
        attempt = {
            "questions": questions,
            "num_questions": num_questions,
            "answers": user_answers,
            "score": correct_answers,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state["attempts"].append(attempt)

# Display previous attempts in the sidebar
for idx, attempt in enumerate(st.session_state["attempts"]):
    if st.sidebar.button(f"Attempt {idx + 1} : {attempt['score']}/{attempt['num_questions']} Correct"):
        st.write(f"### Attempt {idx + 1} - {attempt['score']}/{attempt['num_questions']} Correct")
        st.write(f"Time: {attempt['timestamp']}")
        for i, question in enumerate(attempt['questions']):
            st.write(f"### Question {i + 1}: {question['question']}")
            st.write(f"**Your answer**: {', '.join(attempt['answers'][i])}")
            st.write(f"**Correct answer**: {question['answer']}")
            st.write(f"**Explanation**: {question['answer_explanation']}")
