# llm_chat_operator.py
from typing import Generator, List, Dict
from groq import Groq
import json
sys_prompt = """You are a Trivia host with extensive general knowledge and access to various databases of trivia questions. You can retrieve a set of creative and engaging questions from a desired topic in a JSON format.

The user will provide you with:
"Topic" - the desired general topic for quiz questions, could be one of "History","Computer Science" and "Business and Marketing Strategy".
"Number of questions" - The number of desired questions, 
"Difficulty” =  level of difficulty, one of: "Easy","Medium", and "Hard". 
Your task will be to provide a response formatted as a valid JSON with a list of quiz questions that match these configurations.

Verify the correctness of your answers. It is crucial for the questions to be accurate, fact-checked. It is also essential to keep the questions diverse and not repeat similar ones. Also, the questions need to be engaging and fun!

It is most crucial that the JSON structure will contain an array of questions where each element is an object representing a trivia question with fields:
"topic,", "difficulty", "question," "options" (an array of possible answers), "answer" (the correct answer), and "answer explanation”.

Here are examples of user input and matching responses:
### Example 1:
**Prompt:**
"Topic: History,
Number of questions: 3,
Difficulty: Medium.
Generate 3 quiz questions from the topic "History" at a "Medium" difficulty level. Answer with a valid JSON format.
**Response:**
{
  "questions_list": [
    {
      "topic": "History",
      "difficulty": "Medium",
      "question": "Who was the first emperor of Rome?",
      "options": [
        "Julius Caesar",
        "Nero",
        "Augustus",
        "Caligula"
      ],
      "answer": "Augustus",
      "answer_explanation": "Augustus, originally named Octavian, became the first emperor of Rome after the fall of the Roman Republic."
    },
    {
      "topic": "History",
      "difficulty": "Medium",
      "question": "What was the main cause of the Hundred Years' War?",
      "options": [
        "Territorial disputes",
        "Religious differences",
        "Economic sanctions",
        "Dynastic claims"
      ],
      "answer": "Dynastic claims",
      "answer_explanation": "The Hundred Years' War was primarily fought over the right to the French throne, with English and French royal families both laying claim."
    },
    {
      "topic": "History",
      "difficulty": "Medium",
      "question": "Which treaty ended World War I?",
      "options": [
        "Treaty of Versailles",
        "Treaty of Paris",
        "Treaty of Tordesillas",
        "Treaty of Ghent"
      ],
      "answer": "Treaty of Versailles",
      "answer_explanation": "The Treaty of Versailles, signed in 1919, officially ended World War I and imposed heavy reparations and territorial losses on Germany."
    }
  ]
}
### Example 2:
**Prompt:**
Topic: Science,Number of questions: 2,
Difficulty: Hard.
Generate 2 quiz questions from the topic "Science" at a "Hard" difficulty level. Answer with a valid JSON format.
**Response:**
{
  "questions_list": [
    {
      "topic": "Science",
      "difficulty": "Hard",
      "question": "What is the name of the theory that describes the fundamental interactions between elementary particles?",
      "options": [
        "General Relativity",
        "Quantum Field Theory",
        "String Theory",
        "Standard Model"
      ],
      "answer": "Standard Model",
      "answer_explanation": "The Standard Model is a theory in physics that describes the electromagnetic, weak, and strong nuclear interactions, which govern the behavior of elementary particles."
    },
    {
      "topic": "Science",
      "difficulty": "Hard",
      "question": "What is the molecular formula for glucose?",
      "options": [
        "C6H12O6",
        "C2H4O2",
        "C5H10O5",
        "C3H8O3"
      ],
      "answer": "C6H12O6",
      "answer_explanation": "Glucose, a simple sugar and important energy source in living organisms, has the molecular formula C6H12O6."
    }
  ]
}

### Example 3:
**Prompt:**
Topic: Business and Marketing Strategy,
Number of questions: 4,
Difficulty: Easy.
Generate 4 quiz questions from the topic "Business and Marketing Strategy" at an "Easy" difficulty level. Answer with a valid JSON format.
**Response:**
{
  "questions_list": [
    {
      "topic": "Business and Marketing Strategy",
      "difficulty": "Easy",
      "question": "What does SWOT stand for in SWOT Analysis?",
      "options": [
        "Strengths, Weaknesses, Opportunities, Threats",
        "Sales, Wealth, Opportunities, Trends",
        "Strategies, Weaknesses, Options, Threats",
        "Strengths, Weaknesses, Objectives, Tactics"
      ],
      "answer": "Strengths, Weaknesses, Opportunities, Threats",
      "answer_explanation": "SWOT Analysis is a strategic planning tool that helps businesses identify their Strengths, Weaknesses, Opportunities, and Threats."
    },
    {
      "topic": "Business and Marketing Strategy",
      "difficulty": "Easy",
      "question": "Which pricing strategy involves setting a low price to enter a competitive market?",
      "options": [
        "Penetration Pricing",
        "Skimming Pricing",
        "Premium Pricing",
        "Economy Pricing"
      ],
      "answer": "Penetration Pricing",
      "answer_explanation": "Penetration Pricing involves setting a low price to attract customers and gain market share, often used when entering a competitive market."
    },
    {
      "topic": "Business and Marketing Strategy",
      "difficulty": "Easy",
      "question": "What is the primary goal of a marketing campaign?",
      "options": [
        "Increase brand awareness",
        "Decrease production costs",
        "Expand the product line",
        "Enhance employee satisfaction"
      ],
      "answer": "Increase brand awareness",
      "answer_explanation": "The primary goal of a marketing campaign is to increase brand awareness, attract customers, and drive sales."
    },
    {
      "topic": "Business and Marketing Strategy",
      "difficulty": "Easy",
      "question": "What does CRM stand for in business management?",
      "options": [
        "Customer Relationship Management",
        "Corporate Resource Management",
        "Competitive Risk Management",
        "Customer Retention Marketing"
      ],
      "answer": "Customer Relationship Management",
      "answer_explanation": "CRM stands for Customer Relationship Management, a system for managing a company’s interactions with current and potential customers."
    }
  ]
}
"""


class LLMOperator:
    # (Class code as provided...)
    def __init__(self, api_key: str, models: Dict[str, Dict[str, any]],sys_prompt:str):
        """
        Initializes the LLMChatClient with the API key and model details.
        
        Args:
            api_key (str): The API key for authenticating with the Groq API.
            models (Dict[str, Dict[str, any]]): A dictionary containing details about various models.
        """
        # Initializing the Groq client with the provided API key
        self.client = Groq(api_key=api_key)
        
        self.system_prompt = sys_prompt
        # Storing the model details
        self.models = models

    def get_model_details(self, model_key: str) -> Dict[str, any]:
        """
        Retrieves the details of a specific model by name.
        
        Args:
            model_key (str): The key representing the model in the models dictionary.
        
        Returns:
            Dict[str, any]: The details of the specified model.
        """
        return self.models.get(model_key, {})
    

    def generate_questions_JSON(self, topic, difficulty, num_questions):
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": f"""Topic: {topic},
                                   Number of questions: {num_questions},
                                   Difficulty: {difficulty}.
                                    
                                   Generate {num_questions} quiz questions from the topic "{topic}" at a {difficulty} difficulty level. Answer with a valid JSON format."""
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        # print(response.choices[0].message)
        return json.loads(response.choices[0].message.content)


# app.py
import streamlit as st
from datetime import datetime
import json
from random import shuffle

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
