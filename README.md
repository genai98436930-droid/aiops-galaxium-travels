# 🚀 Galaxium Travels — Agentic Flight System (V1)

A FastAPI-based agentic backend system that routes natural language requests into deterministic tool executions (flights, bookings, users).

---

## 📌 Overview

This system exposes a single intelligent endpoint:


Instead of calling multiple APIs directly, users send natural language input and the system:

- Interprets intent (router / optional LLM)
- Maps it to a tool
- Executes backend logic
- Returns structured output

---

## 🧠 Architecture (High-Level)

```mermaid
flowchart TD
    Client --> API[/api/agent/]
    API --> Engine[Orchestration Engine]
    Engine --> Router[Agent Router]
    Router --> Runtime[Tool Runtime]
    Runtime --> Services[Business Services]
    Services --> DB[(Database)]

## ⚙️ Tech Stack
- FastAPI
- Python 3.11+
- Uvicorn
- Optional LLM (OpenAI / Ollama)
- Custom tool registry system

## 📦 Project Structure
backend/
├── server.py
├── agents/
│   ├── runtime/
│   ├── llm/
│   └── core/
├── orchestration/
├── services/
├── tests/

## 🚀 Getting Started
### Install dependencies
pip install -r requirements.txt

### Run backend
cd backend
python server.py

## 📌 Core Endpoint
POST /api/agent

{
  "input": "show flights"
}

