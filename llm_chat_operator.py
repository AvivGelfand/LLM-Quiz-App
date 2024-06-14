# llm_chat_operator.py

from typing import Generator, List, Dict
from groq import Groq

class LLMOperator:
    """
    A client class to handle interactions with the Groq API.
    
    Attributes:
        client (Groq): The Groq API client initialized with the provided API key.
        models (Dict[str, Dict[str, any]]): A dictionary containing model details.
    """
    
    def __init__(self, api_key: str, models: Dict[str, Dict[str, any]]):
        """
        Initializes the LLMChatClient with the API key and model details.
        
        Args:
            api_key (str): The API key for authenticating with the Groq API.
            models (Dict[str, Dict[str, any]]): A dictionary containing details about various models.
        """
        # Initializing the Groq client with the provided API key
        self.client = Groq(api_key=api_key)

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
    
    def generate_quiz_questions(self, topic, difficulty, num_questions):
    # def create_chat_completion(self, model: str, messages: List[Dict[str, str]], max_tokens: int):

        """
        Creates a chat completion using the Groq API.
        
        Args:
            model (str): The model key to be used for generating responses.
            messages (List[Dict[str, str]]): A list of messages representing the chat history.
            max_tokens (int): The maximum number of tokens to be used for the response.
        
        Returns:
            Generator: A generator yielding the chat completion response.
        """
        return self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Trivia!!"
                },
                {
                    "role": "user",
                    "content": ""
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        # return self.client.chat.completions.create(
        #     model=model,
        #     messages=messages,
        #     max_tokens=max_tokens,
        #     stream=True
        # )


        
    def generate_chat_responses(self, chat_completion) -> Generator[str, None, None]:
        """
        Generates chat responses from the Groq API response.
        
        Args:
            chat_completion: The response object from the Groq API.
        
        Yields:
            str: The content of each response chunk.
        """
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content



# example usage in app.py
models = {
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}
# Initialize the LLMChatClient with the provided API key and model details
llm_operator = LLMOperator(api_key=st.secrets["GROQ_API_KEY"], models=models)

import streamlit as st

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
num_questions = st.slider("Number of quiz questions", min_value=1, max_value=8, value=5)

# Select quiz topic
topic = st.selectbox("Select quiz topic", ["Science", "History", "Geography"])

# Select difficulty level
difficulty = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])

sys_prompt = """You are a Trivia host with extensive general knowledge and access to various databases of trivia questions. You can retrieve a set of creative and engaging questions from a desired topic in a JSON format.

The user will provide you with:
"Topic" - the desired general topic for quiz questions, could be one of "Geography", "History" - "Science","Business and Marketing Strategy" , or "Large Language Models and AI Assistants".
"Number of questions" - The number of desired questions, 
"Difficulty” =  level of difficulty, one of: "Easy","Medium", and "Hard". 
Your task will be to provide a response formatted as a valid JSON with a list of quiz questions that match these configurations.

Verify the correctness of your answers. It is crucial for the questions to be accurate, fact-checked. It is also essential to keep the questions diverse and not repeat similar ones. Also, the questions need to be engaging and fun!

It is most crucial that the JSON structure will contain an array of questions where each element is an object representing a trivia question with fields:
"topic,", "difficulty", "question," "options" (an array of possible answers), "answer" (the correct answer), and "answer explanation”.

Here are examples of user input and matching responses:
### Example 1:
**Prompt:**
"Topic: History,\nNumber of questions: 3,\nDifficulty: Medium.\nGenerate 3 quiz questions from the topic "History" at a "Medium" difficulty level. Answer with a valid JSON format.
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
Topic: Science,n\Number of questions: 2,\nDifficulty: Hard.\n\nGenerate 2 quiz questions from the topic "Science" at a "Hard" difficulty level. Answer with a valid JSON format.
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
Topic: Business and Marketing Strategy,\nNumber of questions: 4,\nDifficulty: Easy.\n\nGenerate 4 quiz questions from the topic "Business and Marketing Strategy" at an "Easy" difficulty level. Answer with a valid JSON format.
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
# Generate questions button
if st.button("Generate Questions"):
    questions = llm_operator.generate_quiz_questions(num_questions, topic, difficulty)
    history.append({"topic": topic, "difficulty": difficulty, "questions": questions})
    conversation_history.write(history)

    # Display generated questions
    st.subheader("Generated Quiz Questions")
    for question in questions:
        st.write(question)

# assumming all buttons are set
if st.button("Generate Questions"):
    messages = [
        {
            "role": "user",
             "content": f"Generate {num_questions} {topic} questions of {difficulty} difficulty."
        }
        ]

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.create_chat_completion(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = client.generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})
        
