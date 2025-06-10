let websocket = null;
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const transcriptDiv = document.querySelector('#transcript .content');
const responseDiv = document.querySelector('#response .content');
const statusDiv = document.getElementById('status');

// Connect to WebSocket
function connectWebSocket() {
    websocket = new WebSocket('ws://localhost:8000/ws/audio-stream');
    
    websocket.onopen = function(event) {
        console.log('WebSocket connected');
        statusDiv.textContent = '✅ Connected to Medical Assistant';
        statusDiv.className = 'status connected';
        startBtn.disabled = false;
    };
    
    websocket.onmessage = function(event) {
        if (event.data instanceof Blob) {
            // Handle audio response
            const audioUrl = URL.createObjectURL(event.data);
            const audio = new Audio(audioUrl);
            audio.play().catch(e => console.error('Error playing audio:', e));
        } else {
            // Handle JSON response
            try {
                const data = JSON.parse(event.data);
                if (data.transcript) {
                    transcriptDiv.textContent = data.transcript;
                }
                if (data.response) {
                    responseDiv.textContent = data.response;
                }
                if (data.error) {
                    responseDiv.textContent = '❌ Error: ' + data.error;
                }
            } catch (e) {
                responseDiv.textContent = event.data;
            }
        }
    };
    
    websocket.onclose = function(event) {
        console.log('WebSocket disconnected');
        statusDiv.textContent = '❌ Disconnected';
        statusDiv.className = 'status';
        startBtn.disabled = true;
        stopBtn.disabled = true;
    };
    
    websocket.onerror = function(error) {
        console.error('WebSocket error:', error);
        statusDiv.textContent = '⚠️ Connection error';
        statusDiv.className = 'status';
    };
}

// Initialize audio recording
async function initAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: { 
                sampleRate: 16000,
                channelCount: 1,
                echoCancellation: true,
                noiseSuppression: true
            } 
        });
        
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        
        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];
            
            // Convert to array buffer and send
            audioBlob.arrayBuffer().then(buffer => {
                if (websocket && websocket.readyState === WebSocket.OPEN) {
                    websocket.send(buffer);
                }
            });
            
            statusDiv.innerHTML = '<span class="loading"></span>Processing your question...';
            statusDiv.className = 'status';
        };
        
        return true;
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Error accessing microphone. Please allow microphone access.');
        return false;
    }
}

// Start recording
startBtn.onclick = async function() {
    if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        alert('Please wait for connection to be established');
        return;
    }
    
    if (!mediaRecorder) {
        const success = await initAudio();
        if (!success) return;
    }
    
    if (!isRecording) {
        mediaRecorder.start();
        isRecording = true;
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusDiv.textContent = '🎙️ Recording... Speak your medical question';
        statusDiv.className = 'status recording';
        transcriptDiv.textContent = '👂 Listening...';
    }
};

// Stop recording
stopBtn.onclick = function() {
    if (isRecording && mediaRecorder) {
        mediaRecorder.stop();
        isRecording = false;
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
};

// Initialize connection when page loads
window.onload = function() {
    connectWebSocket();
};

// Cleanup on page unload
window.onbeforeunload = function() {
    if (websocket) {
        websocket.close();
    }
};