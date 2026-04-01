# BriefNote

BriefNote is a lightweight AI note-taking app with a Google-Docs-like writing experience.  
You write notes in a document editor, then use an AI sidebar to ask questions, summarize, rewrite selections, and extract useful information from the current note context.

## Current MVP Scope

- Single-user note-taking app
- Left sidebar for documents
- Center editor for writing notes
- Right AI panel for note-aware actions
- AI uses selected text when available, otherwise the current document
- FastAPI backend + React frontend
- SQLite for local persistence

## Tech Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy + SQLite
- Editor: Tiptap (or textarea in early scaffold stages)
- AI: Backend-mediated provider integration
- Styling: Plain CSS

## Project Structure

```text
briefnote/
├── frontend/
├── backend/
├── AGENTS.md
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+ or 3.12+
- Git

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
uvicorn main:app --reload
```

The backend should start on something like:

```text
http://127.0.0.1:8000
```

## Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend should start on something like:

```text
http://localhost:5173
```

## Environment Variables

Create a local `.env` file when needed for AI integration.

Example:

```env
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Do not commit your real `.env` file. Commit only `.env.example` if you add one later.

## Current Status

This repo currently contains the initial MVP scaffold.  
The next steps are:

- finish document CRUD flow
- improve editor experience
- add AI chat endpoint
- stream AI responses into the sidebar
- support insert / replace actions from AI output

## Notes

- The app should remain usable without AI.
- The first version intentionally avoids auth, collaboration, and vector search.
- Project workflow instructions for OpenCode live in `AGENTS.md` and related markdown files.

## License

MIT
