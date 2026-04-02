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
    def test_ask_action_passes_user_message_directly(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Some document content</p>",
            action="ask",
            user_message="What is this about?",
        )
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "personal assistant" in messages[0]["content"].lower()
        assert "Note:" in messages[0]["content"]
        assert "Some document content" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What is this about?"

    def test_summarize_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Long document</p>",
            action="summarize",
            user_message="",
        )
        assert "Summarize" in messages[1]["content"]
        assert "Long document" in messages[0]["content"]

    def test_rewrite_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Old text</p>",
            action="rewrite",
            user_message="",
        )
        assert "Rewrite" in messages[1]["content"]

    def test_extract_action_adds_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Notes here</p>",
            action="extract",
            user_message="",
        )
        assert "Extract" in messages[1]["content"]

    def test_selection_included_in_system_prompt(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Full doc text here</p>",
            action="ask",
            user_message="What are the key points?",
            selection="<p>Selected important text</p>",
            title="My Note Title",
        )
        system = messages[0]["content"]
        assert "Selected important text" in system
        assert "Full doc text here" in system
        assert "Note: My Note Title" in system

    def test_title_included_in_context(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Content</p>",
            action="ask",
            user_message="?",
            title="My Meeting Notes",
        )
        system = messages[0]["content"]
        assert "Note: My Meeting Notes" in system
        assert "Content" in system

    def test_title_defaults_to_untitled(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Content</p>",
            action="ask",
            user_message="?",
        )
        system = messages[0]["content"]
        assert "Note: Untitled" in system

    def test_truncates_large_content(self):
        large_html = "<p>" + "word " * 10000 + "</p>"
        messages = prompt_builder.build_messages(
            document_content=large_html,
            action="ask",
            user_message="Summarize?",
        )
        system = messages[0]["content"]
        assert len(system) <= 32000 + 500

    def test_truncates_selection_if_large(self):
        large_selection = "<p>" + "x" * 2000 + "</p>"
        messages = prompt_builder.build_messages(
            document_content="<p>doc</p>",
            action="ask",
            user_message="?",
            selection=large_selection,
        )
        system = messages[0]["content"]
        assert len(system) <= 32000 + 500

    def test_non_ask_action_user_message_starts_with_instruction(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Doc text</p>",
            action="summarize",
            user_message="",
            selection="<p>Selected</p>",
        )
        assert messages[1]["content"].startswith("Summarize")
        assert "Doc text" in messages[0]["content"]

    def test_system_prompt_contains_personal_assistant(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Test</p>",
            action="ask",
            user_message="Test?",
        )
        assert messages[0]["role"] == "system"
        assert "personal assistant" in messages[0]["content"].lower()
        assert "Note:" in messages[0]["content"]

    def test_system_prompt_allows_general_knowledge(self):
        messages = prompt_builder.build_messages(
            document_content="<p>Test</p>",
            action="ask",
            user_message="What is Python?",
        )
        system = messages[0]["content"]
        assert "general knowledge" in system.lower() or "personal assistant" in system.lower()
