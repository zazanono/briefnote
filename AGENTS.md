# AGENTS.md

## Project
Single-user AI note-taking web app with a Google-Docs-like writing experience and an AI sidebar/chat that uses note context.

## Product rules
- The editor is the primary experience; AI is secondary.
- Default AI scope is the current document.
- If the user has a text selection, AI actions should prefer the selected text as primary context.
- The app must remain fully usable without AI.
- Keep the MVP single-user unless explicitly asked to add collaboration.
- Do not add embeddings, vector databases, or full RAG unless requested.
- Prefer clear UX over feature count.
- Favor boring, maintainable implementations.

## MVP features
- Document list in a left sidebar.
- Main rich-text editor in the center.
- Right AI panel with Ask, Summarize, Rewrite, and Extract action items.
- Autosave documents.
- Create, rename, delete documents.
- AI endpoint that answers only from the current document or current selection.
- Streaming AI responses in the sidebar.

## Non-goals for the first version
- Multi-user collaboration.
- Google Docs import/export fidelity.
- Voice mode.
- Multi-document search.
- Background indexing.
- Authentication beyond simple local dev setup.

## Preferred stack
- Frontend: React + TypeScript + Vite.
- Editor: Tiptap.
- Styling: Tailwind CSS or clean CSS modules.
- Backend: FastAPI.
- Database: SQLite.
- AI provider abstraction: start with OpenAI-compatible API shape, allow Ollama later.

## Architecture rules
- Keep frontend and backend separate.
- The frontend must never contain secret API keys.
- All AI calls go through the backend.
- Prompt building must live in a dedicated backend service/module.
- Document persistence must be abstracted behind a small repository/service layer.
- Use typed request/response contracts.
- Avoid introducing state management libraries unless clearly necessary.

## UX rules
- Make it obvious what context the AI is using: selected text vs whole document.
- AI responses should offer actions: insert into doc, replace selection, copy.
- Never auto-modify user content without explicit confirmation.
- Keep the editor fast and uncluttered.
- Use loading and error states that do not block writing.

## Prompting rules
- Instruct the model to answer only from provided document context.
- If the document does not contain the answer, the model should say so.
- Separate system instructions, context payload, and user request cleanly.
- Keep prompt assembly testable.

## Code quality
- Prefer small files and focused components.
- Write concise comments only where needed.
- Add tests for backend prompt construction and core API behavior.
- Keep naming literal and unsurprising.
- Refactor only when duplication is real, not speculative.

## Working style for OpenCode
- Start with a plan before large changes.
- Break work into small, testable steps.
- After each feature, run the relevant tests and fix issues before moving on.
- Explain tradeoffs briefly when proposing architecture changes.
- Do not silently add major dependencies.
