import re
from typing import Literal

Action = Literal["ask", "summarize", "rewrite", "extract"]

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer ONLY using the provided document context. "
    "If the context does not contain enough information to answer, say so explicitly. "
    "Do not make up information. Keep responses concise and relevant."
)

ACTION_INSTRUCTIONS: dict[Action, str] = {
    "summarize": "Summarize the following text concisely:",
    "rewrite": "Rewrite the following text to improve clarity and flow:",
    "extract": "Extract the key information and main points from the following:",
}


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_messages(
    document_content: str,
    action: Action,
    user_message: str,
    selection: str | None = None,
    max_chars: int = 32000,
) -> list[dict]:
    doc_text = strip_html(document_content)
    if len(doc_text) > max_chars:
        doc_text = doc_text[:max_chars]

    if selection:
        context = f"SELECTED TEXT:\n{strip_html(selection)}\n\nDOCUMENT CONTENT:\n{doc_text}"
    else:
        context = f"DOCUMENT CONTENT:\n{doc_text}"

    system = {"role": "system", "content": SYSTEM_PROMPT}
    context_msg = {"role": "user", "content": context}

    if action == "ask":
        user_content = user_message
    else:
        instruction = ACTION_INSTRUCTIONS[action]
        user_content = f"{instruction}\n\n{context}"

    user_msg = {"role": "user", "content": user_content}

    return [system, context_msg, user_msg]
