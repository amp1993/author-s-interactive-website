import os

class Config:
    # Get the OpenAI API key from the environment variable
    OPENAI_API_KEY = os.getenv("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")

class Database: 
    BASE_URL = os.getenv("http://127.0.0.1:5000/api")