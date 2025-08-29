import os
import logging
import json
from datetime import datetime
import requests

# Configure logging
log_directory = os.getenv("LOG_DIR", "logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(
    log_directory, f"llm_calls_{datetime.now().strftime('%Y%m%d')}.log"
)

# Set up logger
logger = logging.getLogger("llm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to root logger
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Simple cache configuration
cache_file = "llm_cache.json"


def call_llm(prompt: str, use_cache: bool = True) -> str:
    """
    Calls an Ollama model to generate a text response.

    Args:
        prompt (str): The prompt to send to the model.
        use_cache (bool, optional): Whether to use Ollama's caching mechanism. Defaults to True.

    Returns:
        str: The generated text response from the model.
    """
    try:
        response = ollama.chat(
            model='gemma3:27b',  # deepcoder:14b  gemma3:12b  phi4:14b Replace with your desired Ollama model name
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            stream=False, # important to set stream to false to get the response.
            options = {
                'use_cache': use_cache,
            }

        )
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"Ollama Error: {e}")

if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
