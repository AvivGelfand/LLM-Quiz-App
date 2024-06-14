from typing import Generator, List, Dict
from groq import Groq
import json
from system_prompts import sys_prompt
import random

class LLMOperator:
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
        self.client = Groq(api_key=api_key)
        self.system_prompt = sys_prompt
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

    def generate_questions_JSON(self, topic: str, difficulty: str, num_questions: int) -> Dict[str, any]:
        """
        Generates quiz questions in JSON format based on the provided topic, difficulty, and number of questions.

        Parameters:
        topic (str): The topic for which the quiz questions are to be generated.
        difficulty (str): The difficulty level of the quiz questions.
        num_questions (int): The number of quiz questions to be generated.

        Returns:
        Dict[str, any]: A dictionary containing the generated quiz questions in JSON format.

        Raises:
        ValueError: If the topic, difficulty, or num_questions parameters are invalid.
        """
        # Input validation
        if not isinstance(topic, str) or not isinstance(difficulty, str) or not isinstance(num_questions, int):
            raise ValueError("Invalid input parameters")

        # Model selection based on topic and difficulty
        model = self.select_model(topic, difficulty)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {
                        "role": "user",
                        "content": f"""Topic: {topic},
                                        Number of questions: {num_questions},
                                        Difficulty: {difficulty}.
                                        
                                        Generate {num_questions} quiz questions from the topic "{topic}" at a {difficulty} difficulty level. Answer with a valid JSON format.""",
                    },
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # Handle exceptions
            print(f"Error generating quiz questions: {e}")
            return {}

    def select_model(self, topic: str, difficulty: str) -> str:
        """
        Selects a model based on the topic and difficulty level.

        Parameters:
        topic (str): The topic for which the quiz questions are to be generated.
        difficulty (str): The difficulty level of the quiz questions.

        Returns:
        str: The name of the selected model.
        """
        # Implement logic to select the most suitable model based on topic and difficulty
        # For example, you could use a mapping of topics to models or implement a logic to choose the most suitable model
        return random.choice(list(self.models.keys()))