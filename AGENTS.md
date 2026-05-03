
---

# ✅ 3. AGENTS.md (fully Markdown-safe + cleaned)

```markdown
# AGENTS.md

This is a demo system, not production software.

It is designed to mimic enterprise architecture patterns for AI-native tooling experiments.

---

## ⚠️ Critical Non-Obvious Patterns

### Backend Architecture

- Single entrypoint: `/api/agent`
- Request flow:

server.py → OrchestrationEngine → AgentRouter → ToolRuntime → Services → DB

- Tool registry defines execution mapping:

tool_name → function

- SQLite is the only database
- No external DB dependency

---

## 🧪 Testing Rules

- Uses in-memory SQLite for tests
- Requires session mocking
- Seed data is disabled in test mode

Run tests:

```bash
cd backend
pytest

## 🧪 Testing Rules

- Uses in-memory SQLite for tests
- Requires session mocking
- Seed data is disabled in test mode

Run tests:
```bash
cd backend
pytest

🧩 Tool System
Tools are registered in:
agents/tools/register.py

Tools map directly to service functions

🖥️ Frontend Notes
API base URL:
VITE_API_URL

Error handling uses structured responses

🚀 Commands
Backend tests:
cd backend && pytest

Frontend dev:
cd frontend && npm run dev

Start system:
./start.sh

📌 Design Philosophy
- Deterministic routing
- Minimal orchestration complexity
- Service-layer business logic
- Simple SQLite persistence

⚠️ V1 Limitation
- No multi-step agent planning
- One tool per request

