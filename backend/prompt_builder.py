import re
from typing import Literal

Action = Literal["ask", "summarize", "rewrite", "extract"]

SYSTEM_PROMPT = (
    "You are a helpful personal assistant. "
    "The user's current note is provided below as context. "
    "Use it to give relevant, grounded answers — but you can also draw on "
    "general knowledge when helpful. "
    "If the note is relevant to the question, prioritize it. "
    "If the user asks something unrelated to the note, answer normally "
    "as a personal assistant."
)

ACTION_INSTRUCTIONS: dict[Action, str] = {
    "summarize": "Summarize the key points from this note:",
    "rewrite": "Rewrite the selected text to be clearer and more concise:",
    "extract": "Extract the most useful information from this note:",
}


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _build_note_context(title: str, doc_text: str, selection: str | None) -> str:
    note_header = f"Note: {title}\n{doc_text}"
    if selection:
        return f"Selected text:\n{selection}\n\n{note_header}"
    return note_header


def build_messages(
    document_content: str,
    action: Action,
    user_message: str,
    selection: str | None = None,
    title: str = "Untitled",
    max_chars: int = 32000,
) -> list[dict]:
    doc_text = strip_html(document_content)
    if len(doc_text) > max_chars:
        doc_text = doc_text[:max_chars]

    note_context = _build_note_context(title, doc_text, strip_html(selection) if selection else None)
    system_content = f"{SYSTEM_PROMPT}\n\n{note_context}"

    if action == "ask":
        user_content = user_message
    else:
        instruction = ACTION_INSTRUCTIONS[action]
        user_content = f"{instruction}\n\n{note_context}"

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
