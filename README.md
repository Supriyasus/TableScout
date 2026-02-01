# TableScout

**Discover. Personalize. Book — Seamlessly Everywhere**

TableScout is a developer-friendly, modular platform for building personalized, location-based recommendation and booking systems. It blends real-time signals (traffic, popularity), stored user preferences, and agent-driven intelligence to deliver tailored, explainable recommendations and reliable booking flows.

At its core TableScout uses an agent-based backend and focused MCP (Model Connector Provider) servers:

- **AI Agents**: IntentExtractionAgent converts natural language queries into structured intents; PlannerAgent constructs search strategies; TrafficAgent and PopularityAgent provide real-time context; ScoringAgent ranks results using intent and user preferences; ExplanationAgent generates human-readable rationales.
- **MCP Servers**: MapboxMCP and other MCPs encapsulate external APIs (maps, routing, bookings) behind a uniform interface, keeping external integrations isolated, testable, and replaceable.

This architecture (agents + MCPs) enables fast iteration, clear separation of concerns, and easier testing. The stack (FastAPI backend + React frontend) provides a developer-friendly environment for building and extending location-based experiences.

---

## Key Features

- **Modular backend (FastAPI)** with agent-based scoring and planning
- **React frontend** for a responsive chat-driven discovery UI
- **JWT-based authentication** and per-user personalization
- **Real-time signals** (traffic, popularity, crowd estimation)
- **Extensible maps integration** (Mapbox / Google Maps)

---

## Tech Stack

- Python (FastAPI) — backend
- React (Create React App) — frontend
- PostgreSQL — database
- SQLAlchemy — ORM
- JWT — authentication
- Pytest / Jest — testing

---

## Prerequisites

- Python 3.9+
- Node.js + npm
- PostgreSQL
- Git

---

## Repository Structure

- `backend/` — FastAPI app, agents, DB, and MCPs
- `frontend/` — React app and UI components
- `README.md` — this file

---

## Installation & Setup

1) Clone the repo

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2) Backend

```bash
cd backend
pip install -r requirements.txt
# initialize DB (creates tables)
python -m db.init_db
```

3) Frontend

```bash
cd frontend
npm install
```

## Running Locally

### Start backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

### Start frontend

```bash
cd frontend
npm start
```

App: `http://localhost:3000`

**Enjoy building with TableScout!** 🚀
