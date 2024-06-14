# llm_chat_client.py

from typing import Generator, List, Dict
from groq import Groq

class LLMChatClient:
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

    def create_chat_completion(self, model: str, messages: List[Dict[str, str]], max_tokens: int):
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
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            stream=True
        )

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

