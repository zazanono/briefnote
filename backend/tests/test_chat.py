import json
from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal, get_db

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_chat_messages_are_document_scoped():
    # Create first document
    response = client.post("/api/documents", json={"title": "Doc 1", "content": "Content 1"})
    assert response.status_code == 201
    doc1_id = response.json()["id"]

    # Create second document
    response = client.post("/api/documents", json={"title": "Doc 2", "content": "Content 2"})
    assert response.status_code == 201
    doc2_id = response.json()["id"]

    # Mock the ai_provider stream_chat
    import ai_provider
    original_stream_chat = ai_provider.stream_chat
    def mock_stream_chat(messages, model=None):
        yield "Mock response"
    ai_provider.stream_chat = mock_stream_chat

    try:
        # Send message in doc 1
        chat_request_1 = {
            "document_id": doc1_id,
            "action": "ask",
            "user_message": "Hello from doc 1"
        }
        with client.stream("POST", "/api/ai/chat", json=chat_request_1) as r:
            assert r.status_code == 200
            list(r.iter_lines()) # Consume stream to trigger DB save

        # Send message in doc 2
        chat_request_2 = {
            "document_id": doc2_id,
            "action": "ask",
            "user_message": "Hello from doc 2"
        }
        with client.stream("POST", "/api/ai/chat", json=chat_request_2) as r:
            assert r.status_code == 200
            list(r.iter_lines()) # Consume stream to trigger DB save
            
        # Get chat for doc 1
        response = client.get(f"/api/documents/{doc1_id}/chat")
        assert response.status_code == 200
        chat1 = response.json()
        assert len(chat1) == 2
        assert chat1[0]["role"] == "user"
        assert chat1[0]["content"] == "Hello from doc 1"
        assert chat1[1]["role"] == "assistant"
        assert chat1[1]["content"] == "Mock response"
        
        # Get chat for doc 2
        response = client.get(f"/api/documents/{doc2_id}/chat")
        assert response.status_code == 200
        chat2 = response.json()
        assert len(chat2) == 2
        assert chat2[0]["role"] == "user"
        assert chat2[0]["content"] == "Hello from doc 2"
        assert chat2[1]["role"] == "assistant"
        assert chat2[1]["content"] == "Mock response"

        # Verify chat order
        assert chat1[0]["created_at"] < chat1[1]["created_at"]

    finally:
        # Restore mock
        ai_provider.stream_chat = original_stream_chat


def test_web_grounding_appends_web_block_and_persists_sources():
    # Create a document
    response = client.post("/api/documents", json={"title": "WebDoc", "content": "Doc content for web grounding"})
    assert response.status_code == 201
    doc_id = response.json()["id"]

    # Mock tavily.search and ai_provider.stream_chat and capture messages passed to the provider
    import tavily
    import ai_provider

    original_search = tavily.search
    original_stream_chat = ai_provider.stream_chat

    def mock_search(query, limit=3):
        return [
            {"title": "Result One", "url": "https://example.com/1", "snippet": "Snippet one", "host": "example.com"},
            {"title": "Result Two", "url": "https://example.org/2", "snippet": "Snippet two", "host": "example.org"},
        ]

    captured = {}

    def mock_stream_chat(messages, model=None):
        # capture the messages the server built for the provider
        captured['messages'] = messages
        yield "Web grounded response"

    tavily.search = mock_search
    ai_provider.stream_chat = mock_stream_chat

    try:
        chat_request = {
            "document_id": doc_id,
            "action": "ask",
            "user_message": "What external info is relevant?",
            "web_ground": True,
        }

        with client.stream("POST", "/api/ai/chat", json=chat_request) as r:
            assert r.status_code == 200
            list(r.iter_lines())

        # Ensure provider received messages and that web results were injected into the system prompt
        assert 'messages' in captured
        system = captured['messages'][0]
        assert system['role'] == 'system'
        assert "Web search results" in system['content']

        # Verify persisted chat contains assistant reply and a [WEB_SOURCES] marker
        response = client.get(f"/api/documents/{doc_id}/chat")
        assert response.status_code == 200
        chat = response.json()

        # Expect at least user + assistant + assistant_meta
        roles = [m['role'] for m in chat]
        contents = [m['content'] for m in chat]
        assert 'assistant' in roles
        # find a content that starts with the marker
        assert any(c.startswith('[WEB_SOURCES]') for c in contents)

    finally:
        tavily.search = original_search
        ai_provider.stream_chat = original_stream_chat
