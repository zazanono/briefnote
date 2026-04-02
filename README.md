# BriefNote

<table>
<tr>
<td>

BriefNote is a lightweight AI note-taking app with a Google-Docs-like writing experience.  
You write notes in a document editor, then use an AI sidebar to ask questions, summarize, rewrite selections, and extract useful information from the current note context.

</td>
<td align="right" valign="middle" width="120">
  <img src="./frontend/public/icon-192.svg" alt="BriefNote icon" width="96" height="96" />
</td>
</tr>
</table>

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
- Editor: Tiptap
- AI: Backend-mediated OpenRouter integration (OpenAI-compatible streaming API)
- Styling: Plain CSS

## Project Structure

```text
briefnote/
├── frontend/
├── backend/
│   ├── prompt_builder.py
│   ├── ai_provider.py
│   └── main.py
├── AGENTS.md
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+ or 3.12+
- Git
- An [OpenRouter](https://openrouter.ai) API key (free account works)

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
uvicorn main:app --reload
```

The backend starts on:

```
http://127.0.0.1:8000
```

## Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend starts on:

```
http://localhost:5173
```

## Environment Variables

Create a `backend/.env` file for AI integration:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=qwen/qwen3.6-plus-preview:free
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys).  
The default model is `qwen/qwen3.6-plus-preview:free` which is currently free on OpenRouter.  
Do not commit your real `.env` file. A `.env.example` is provided.

## Current Status

- ✅ Document CRUD (create, rename, delete)
- ✅ Tiptap editor with autosave
- ✅ AI panel with streaming responses via OpenRouter
- ✅ Ask / Summarize / Rewrite / Extract actions
- ✅ Insert at cursor and Replace selection from AI output
- 🔲 Voice input
- 🔲 Auth and multi-user support
- 🔲 Local model support (Ollama)

## Notes

- The app is fully usable without AI (document CRUD and editing work independently).
- The first version intentionally avoids auth, collaboration, and vector search.
- AI answers are grounded in the current note context.
- Project workflow instructions for OpenCode live in `AGENTS.md`.

## License

Apache License 2.0
