# AURA — AI Unified Reasoning Assistant

AURA is a full-stack AI assistant that uses **Generative AI, LangGraph, LangChain, RAG, REST APIs and multi-agent routing** to handle different types of user requests through a single interface.

The project is designed as a practical demonstration of how modern AI applications can combine LLMs, agents, document retrieval, APIs, authentication and web technologies.

---

## 🚀 Features

- 🤖 Generative AI chatbot
- 🧠 LangGraph-based workflow orchestration
- 🔀 Intelligent request routing
- 👨‍💻 Coding Agent for programming questions
- 📚 Research Agent with RAG
- 💬 General AI Agent
- 🔗 External REST API tools
- 🐙 GitHub REST API integration
- 🔐 API-key authentication
- 📄 PDF document processing
- 🔎 Semantic document search
- 🗃️ FAISS vector database
- 🌐 Node.js + Express web server
- ⚡ FastAPI backend
- 🎨 Responsive web UI
- 🔄 Git/GitHub version control

---

## 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                HTML / CSS / JavaScript
                           │
                           ▼
                   Node.js + Express
                     Web Layer
                           │
                        HTTP/JSON
                           │
                           ▼
                       FastAPI
                    AI Backend/API
                           │
                           ▼
                       LangGraph
                  Workflow Orchestration
                           │
                           ▼
                    Intent Router
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       General          Research          Coding
        Agent             Agent            Agent
          │                │                 │
          │                ├── RAG           │
          │                └── FAISS         │
          │                                  │
          └────────────────┬─────────────────┘
                           ▼
                       LangChain
                           │
                           ▼
                     Gemini LLM
                           │
                           ▼
                    Response / Tool
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                      Node.js
                           │
                           ▼
                         USER


🧠 AI Workflow

AURA first receives the user's request through the web interface.

The request follows this flow:

User sends a message.
Node.js receives the request.
Node.js forwards the request to FastAPI.
FastAPI invokes the LangGraph workflow.
LangGraph sends the request to the router.
The router classifies the request.
The appropriate agent handles the request.
The agent may use:
Gemini LLM
RAG retrieval
FAISS vector store
External REST APIs
The final response is returned to the user.