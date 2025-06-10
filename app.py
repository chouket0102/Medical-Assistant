from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from src.voice.websocket import router as websocket_router

app = FastAPI(title="Medical Voice Assistant")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include WebSocket router
app.include_router(websocket_router)

@app.get("/", response_class=HTMLResponse)
async def get_voice_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    print("Starting Medical Voice Assistant...")
    print("Open your browser and go to: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)