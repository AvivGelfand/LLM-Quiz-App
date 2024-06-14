# llmoperator.py

from typing import Generator, List, Dict
from groq import Groq
import json
from system_prompts import sys_prompt

class LLMOperator:
    # (Class code as provided...)
    def __init__(self, api_key: str, models: Dict[str, Dict[str, any]], sys_prompt: str):
        """
        Initializes the LLMOperator with the API key and model details.

        Args:
            api_key (str): The API key for authenticating with the Groq API.
            models (Dict[str, Dict[str, any]]): A dictionary containing details about various models.
            sys_prompt (str): The system prompt to be used for LLM model.

        Returns:
            None
        """
        # Initializing the Groq client with the provided API key
        self.client = Groq(api_key=api_key)

        # Storing the system prompt
        self.system_prompt = sys_prompt

        # Storing the model details
        self.models = models

    def get_model_details(self, model_key: str) -> Dict[str, any]:
        """
        Retrieves the details of a specific model by name.

        Parameters:
        model_key (str): The key representing the model in the models dictionary.

        Returns:
        Dict[str, any]: The details of the specified model. If the model_key is not found in the models dictionary, an empty dictionary is returned.

        Raises:
        None

        """
        return self.models.get(model_key, {})
        

    def generate_questions_JSON(self, topic, difficulty, num_questions):
        """
        Generates quiz questions in JSON format based on the provided topic, difficulty, and number of questions.

        Parameters:
        topic (str): The topic for which the quiz questions are to be generated.
        difficulty (str): The difficulty level of the quiz questions.
        num_questions (int): The number of quiz questions to be generated.

        Returns:
        dict: A dictionary containing the generated quiz questions in JSON format.

        Raises:
        None

        Note:
        This method uses the Groq API to generate the quiz questions. The LLM model used is "llama3-8b-8192".
        The system prompt is passed as a parameter to the LLM model.
        The generated JSON format includes the quiz questions and their corresponding answers.
        """
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
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
        
