from elevenlabs import ElevenLabs
from groq import Groq
from dotenv import load_dotenv
from .settings import get_settings  # Add this import

load_dotenv()
settings = get_settings()  # Add this line



# ElevenLabs Client
elevenlabs_client = None

# Groq Client
groq_client = None

# ElevenLabs
def connect_elevenlabs():
    global elevenlabs_client
    if elevenlabs_client is None:
        elevenlabs_client = ElevenLabs(api_key=settings.ELEVEN_LABS_API_KEY)
    return elevenlabs_client


def get_elevenlabs_client():
    connect_elevenlabs()
    voice_client = elevenlabs_client
    return voice_client


# Groq
def connect_groq():
    global groq_client
    if groq_client is None:
        groq_client = Groq(api_key=settings.GROQ_API_KEY)
    return groq_client


def get_groq_client():
    connect_groq()
    groq = groq_client
    return groq