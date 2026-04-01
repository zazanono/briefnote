# First 10 OpenCode Prompts

Use these one at a time. Wait for each step to finish, review the diff, run the app, then continue.

## 1. Bootstrap the repo
Create a monorepo for a single-user AI notes app named `ai-notes`. Add `apps/web` with Vite + React + TypeScript and `apps/api` with FastAPI. Add a root README, `.env.example`, and root scripts for running frontend and backend together. Follow `AGENTS.md` exactly and keep the setup minimal.

## 2. Add the basic app shell
Implement a three-pane layout in the web app: a left document sidebar, a center editor area placeholder, and a right AI panel placeholder. Use a clean Google-Docs-like layout with simple styling and responsive behavior. Do not add AI logic yet.

## 3. Add document persistence
In the backend, add SQLite-backed document storage with fields: `id`, `title`, `content`, `created_at`, and `updated_at`. Implement endpoints to list, create, fetch, update, rename, and delete documents. Add matching typed API utilities in the frontend.

## 4. Connect the sidebar to real documents
Replace the frontend placeholders so the left sidebar can create documents, switch between them, rename them, and delete them using the backend API. The center panel should load the selected document and show its title and content.

## 5. Integrate Tiptap
Replace the center content textarea/placeholder with a Tiptap editor. Keep the formatting minimal for now: paragraph, bold, italic, bullet list, heading. Implement debounced autosave to the backend and show save status in the UI.

## 6. Add the AI panel UI
Build the right sidebar as an AI panel with tabs or buttons for Ask, Summarize, Rewrite, and Action Items. Add inputs for user request and a visible scope indicator that says either `Selected text` or `Whole document`. Do not call a model yet; just wire the UI state.

## 7. Implement prompt building and AI endpoint
In the backend, add an `/api/ai/ask` endpoint that accepts document id, optional selected text, action type, and user message. Build prompts in a dedicated module. The prompt must instruct the model to answer only from the provided note context and say clearly when the answer is not in the notes. For now, define the provider behind a small interface.

## 8. Wire the AI panel to the backend
Connect the AI panel to the new backend endpoint. Send selected text if present; otherwise send the whole current document. Stream or progressively display the response in the sidebar if convenient, otherwise return a normal response first. Show loading and error states clearly.

## 9. Add insertion actions
Let the user insert an AI answer into the document, replace the current selection with a rewritten version, or copy the answer. Require explicit user action before modifying the document. Keep the interaction simple and predictable.

## 10. Harden and review
Add basic backend tests for prompt construction and the AI route. Add frontend polish for empty states, loading states, and save indicators. Then run a review pass against `AGENTS.md` and summarize anything that is overengineered or missing for the MVP.
