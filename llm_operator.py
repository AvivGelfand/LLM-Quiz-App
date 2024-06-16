from typing import Any, Dict
from groq import Groq
import json
from prompts import sys_prompt, make_user_prompt
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Define the LLMOperator class
class LLMOperator:
    def __init__(self, api_key: str,  sys_prompt: str):
        """
        Initializes the LLMOperator with the API key and model details.

        Args:
            api_key (str): The API key for authenticating with the LLM API.
            models (Dict[str, Dict[str, Any]]): A dictionary containing details about various models.
            sys_prompt (str): The system prompt to be used for LLM model.

        Returns:
            None
        """
        self.api_key = api_key
        self.sys_prompt = sys_prompt



# Modify the GroqOperator class to inherit from LLMOperator
class GroqOperator(LLMOperator):
    def __init__(self, api_key: str,  sys_prompt: str):
        """
        Initializes the GroqOperator with the API key and model details.

        Args:
            api_key (str): The API key for authenticating with the Groq API.
            models (Dict[str, Dict[str, Any]]): A dictionary containing details about various models.
            sys_prompt (str): The system prompt to be used for LLM model.

        Returns:
            None
        """
        super().__init__(api_key, sys_prompt)
        self.client = Groq(api_key=api_key)
        self.system_prompt = sys_prompt
        self.models = {
            "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
            # "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"}, # uncomment to use another model by groq
        }

    def generate_questions_JSON(self, topic: str, difficulty: str, num_questions: int) -> Dict[str, Any]:
        """
        Generates quiz questions in JSON format based on the provided topic, difficulty, and number of questions.

        Parameters:
        topic (str): The topic for which the quiz questions are to be generated.
        difficulty (str): The difficulty level of the quiz questions.
        num_questions (int): The number of quiz questions to be generated.

        Returns:
        dict: A dictionary containing the generated quiz questions in JSON format.

        Note:
        This method uses the Groq API to generate the quiz questions. The LLM model used.
        The system prompt is passed as a parameter to the LLM model.
        The generated JSON format includes the quiz questions and their corresponding answers.
        """
        model = random.choice(list(self.models.keys()))  # selecting a random model
        logger.info(f"Selected model: {model}")

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": self.sys_prompt
                },
                {
                    "role": "user",
                    "content": make_user_prompt(topic=topic, difficulty=difficulty, num_questions=num_questions)
                }
            ],
            temperature=1,
            # max_tokens=2048,  # uncomment to limit the number of tokens generated for saving costs
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    

    def get_model_details(self, model_key: str) -> Dict[str, Any]:
        """
        Retrieves the details of a specific model by name.

        Parameters:
        model_key (str): The key representing the model in the models dictionary.

        Returns:
        Dict[str, Any]: The details of the specified model. If the model_key is not found in the models dictionary, an empty dictionary is returned.
        """
        return self.models.get(model_key, {})