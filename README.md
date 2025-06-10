# 🏥 Medical Voice Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![RAG](https://img.shields.io/badge/RAG-Powered-purple.svg)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

> An AI-powered medical consultation assistant that combines voice recognition, natural language processing, and retrieval-augmented generation (RAG) to provide accurate medical information through an intuitive voice interface.

## 🌟 Features

- **🎤 Voice-to-Voice Interaction**: Real-time speech recognition and text-to-speech responses
- **🔍 RAG-Powered Responses**: Retrieval-Augmented Generation using medical literature
- **📚 Medical Knowledge Base**: Built on comprehensive medical PDFs and documentation
- **🌐 Modern Web Interface**: Clean, responsive UI with real-time status updates
- **⚡ WebSocket Communication**: Low-latency real-time audio streaming
- **🎯 High Accuracy**: Powered by Pinecone vector database and Hugging Face embeddings
- **📱 Mobile Responsive**: Works seamlessly across all devices

## 🚀 Demo

![Medical Voice Assistant Demo](demo.gif)

*Real-time voice interaction with the medical assistant*

## 🏗️ Architecture

```mermaid
graph TB
    A[User Voice Input] --> B[WebSocket Connection]
    B --> C[Speech Recognition]
    C --> D[Medical Agent]
    D --> E[RAG System]
    E --> F[Query Embedding]
    F --> G[HuggingFace Embeddings]
    G --> H[Pinecone Vector DB]
    H --> I[Retrieved Medical Documents]
    I --> J[Context + Query]
    J --> K[LLM Processing]
    K --> L[Generated Response]
    L --> M[Text-to-Speech]
    M --> N[Audio Response]
    N --> B
    B --> O[User Audio Output]
    
    style A fill:#e1f5fe
    style O fill:#e8f5e8
    style H fill:#fff3e0
    style K fill:#f3e5f5
