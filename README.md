# BriefNote

<table>
<tr>
<td>

BriefNote is a lightweight AI note-taking app with a Google-Docs-like writing experience.  
Write notes in a clean document editor, then use the AI sidebar to ask questions, summarize, rewrite, and extract — all grounded in the current note context.

</td>
<td align="right" valign="middle" width="120">
  <img src="./frontend/public/icon-192.svg" alt="BriefNote icon" width="96" height="96" />
</td>
</tr>
</table>

## Features

- **Document editor** — Tiptap-powered rich text editor with autosave
- **AI sidebar** — ask questions, summarize, rewrite, and extract from the current note
- **Context-aware AI** — uses selected text when available, otherwise the full document
- **Streaming responses** — AI responses stream in real time via OpenRouter
- **Web search mode** — optional AI-assisted web search toggle in the composer
- **Document management** — create, rename, and delete notes from the sidebar
- **Dark mode** — full light/dark theme support
- **Fully offline-capable** — editing and document management work without AI

## UI

The app is structured as three panels:

| Panel | Role |
|---|---|
| Left sidebar | Document list — create, select, rename, delete notes |
| Center editor | Tiptap document — the main writing surface |
| Right AI panel | Context-aware AI tools and conversation |

The center note panel scrolls internally once content exceeds the available height — the rest of the shell remains static. The AI composer at the bottom of the right panel includes a unified input area with action buttons (Summarize, Rewrite, Extract) and a globe icon for toggling web search mode on/off.

## Tech Stack

- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Editor:** Tiptap
- **AI:** OpenRouter integration (OpenAI-compatible streaming API)
- **Styling:** Plain CSS

## Project Structure

```text
briefnote/
├── frontend/
├── backend/
│   ├── prompt_builder.py
│   ├── ai_provider.py
│   └── main.py
├── AGENTS.md
├── DEPLOY.md
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+ or 3.12+
- Git
- An [OpenRouter](https://openrouter.ai) API key (free account works)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
uvicorn main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### Environment Variables

Create a `backend/.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=qwen/qwen3.6-plus-preview:free
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys).  
The default model is `qwen/qwen3.6-plus-preview:free`, currently free on OpenRouter.  
Do not commit your real `.env` — a `.env.example` is provided.

## Status

- ✅ Document CRUD (create, rename, delete)
- ✅ Tiptap editor with autosave
- ✅ AI panel with streaming responses via OpenRouter
- ✅ Ask / Summarize / Rewrite / Extract actions
- ✅ Insert at cursor and Replace selection from AI output
- ✅ Bounded note scroll with polished internal scrollbar
- ✅ Unified AI composer with globe-based web search toggle
- ✅ Dark mode with refined note header and panel hierarchy
- 🔲 Voice input
- 🔲 Auth and multi-user support
- 🔲 Local model support (Ollama)

## Deployment

See [DEPLOY.md](./DEPLOY.md) for deployment instructions.

## License

Apache License 2.0
