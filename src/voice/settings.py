from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.ELEVEN_LABS_API_KEY = os.environ.get('ELEVEN_LABS_API_KEY')  # Fixed typo
        self.GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
        self.GROQ_MODEL = "llama3-8b-8192"
        self.PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def get_settings():
    return Settings()