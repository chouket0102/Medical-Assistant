from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .voice_controller import speech_to_text_controller, text_to_speech_controller
from .agent import MedicalAgent  # Updated import
from .logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.websocket("/ws/audio-stream")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    
    # Use Medical Agent instead of basic Agent
    medical_agent = MedicalAgent()
    
    logger.info("Medical Assistant WebSocket connection established")
    
    # Welcome message - don't process through RAG, just send directly
    welcome_response = "Hello! I'm your medical assistant. How can I help you today?"
    
    tts_audio_bytes = await text_to_speech_controller(welcome_response)
    
    await websocket.send_json({"response": welcome_response})
    await websocket.send_bytes(tts_audio_bytes)
    
    try:
        while True:
            # Wait for raw audio bytes
            audio_bytes = await websocket.receive_bytes()
            logger.debug(f"Received audio bytes: {len(audio_bytes)} bytes")
            
            # Transcribe speech to text
            transcript = await speech_to_text_controller(audio_bytes)
            logger.info(f"User query: {transcript}")
            
            # Get medical response using RAG
            response = await medical_agent.invoque(message=transcript)
            logger.info(f"Medical response: {response}")
            
            # Convert response to speech
            tts_audio_bytes = await text_to_speech_controller(response)
            
            # Send response as JSON and audio
            await websocket.send_json({
                "transcript": transcript,
                "response": response
            })
            await websocket.send_bytes(tts_audio_bytes)
            
    except WebSocketDisconnect:
        logger.info("Medical Assistant WebSocket connection closed")
    except Exception as e:
        logger.error(f"Error in medical assistant: {str(e)}")
        await websocket.send_json({"error": str(e)})