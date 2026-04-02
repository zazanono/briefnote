import pytest
import prompt_builder


class TestStripHtml:
    def test_removes_simple_tags(self):
        assert prompt_builder.strip_html("<p>Hello</p>") == "Hello"

    def test_removes_nested_tags(self):
        assert prompt_builder.strip_html("<div><p><strong>Bold</strong> text</p></div>") == "Bold text"

    def test_preserves_text_between_tags(self):
        assert "Hello" in prompt_builder.strip_html("<p>Hello</p><p>World</p>")

    def test_strips_attributes(self):
        assert prompt_builder.strip_html('<a href="url">Link</a>') == "Link"


class TestBuildMessages:
    def test_ask_action_uses_user_message(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Some document content</p>",
            action="ask",
            user_message="What is this about?",
        )
        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert "DOCUMENT CONTENT" in messages[1]["content"]
        assert messages[2]["role"] == "user"
        assert messages[2]["content"] == "What is this about?"

    def test_summarize_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Long document</p>",
            action="summarize",
            user_message="",
        )
        assert "Summarize" in messages[2]["content"]
        assert "Long document" in messages[1]["content"]

    def test_rewrite_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Old text</p>",
            action="rewrite",
            user_message="",
        )
        assert "Rewrite" in messages[2]["content"]

    def test_extract_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Notes here</p>",
            action="extract",
            user_message="",
        )
        assert "Extract" in messages[2]["content"]

    def test_selection_makes_context_primary(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Full doc text here</p>",
            action="ask",
            user_message="What are the key points?",
            selection="<p>Selected important text</p>",
        )
        context_msg = messages[1]
        assert "SELECTED TEXT" in context_msg["content"]
        assert "Selected important text" in context_msg["content"]
        assert "Full doc text here" in context_msg["content"]

    def test_truncates_large_content(self):
        large_html = "<p>" + "word " * 10000 + "</p>"
        messages = prompt_builder.build_messages(
            document_content=large_html,
            action="ask",
            user_message="Summarize?",
        )
        doc_msg = messages[1]["content"]
        assert len(doc_msg) <= 32000 + 100

    def test_system_prompt_present(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Test</p>",
            action="ask",
            user_message="Test?",
        )
        assert messages[0]["role"] == "system"
        assert "only" in messages[0]["content"].lower() or "context" in messages[0]["content"].lower()
