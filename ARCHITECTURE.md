# 🧠 Galaxium Travels - Architecture (V1)

## Overview

Galaxium Travels is a **tool-based agentic backend system** where natural language requests are routed into deterministic tool executions.

---

## System Architecture

```mermaid
flowchart TD
    Client[Client / curl / frontend] --> API[/api/agent endpoint/]

    API --> Server[server.py]
    Server --> Engine[OrchestrationEngine]
    Engine --> Router[AgentRouter]
    Router --> Runtime[ToolRuntime]

    Runtime --> Registry[ToolRegistry]
    Registry --> ToolMap[agents/tools/register.py]

    ToolMap --> Services[Service Layer]
    Services --> DB[(SQLite Database)]

### 🔧 Core Components
- API Layer
- Single endpoint: /api/agent
- Orchestration Engine
- Controls execution flow
- Agent Router
  Maps user input → tool name
- Tool Runtime
  Executes selected tool safely
- Tool Registry
  Maps tool names → functions
- Services Layer
  Business logic layer
  Direct DB access

## 🧩 Design Principles
Tools = execution layer
Services = business logic
Router = decision layer
Runtime = execution layer
## ⚠️ V1 Constraint
One request → one tool execution
Deterministic routing only