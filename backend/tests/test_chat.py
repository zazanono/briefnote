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
