import json
import uuid
from datetime import datetime, timezone
from typing import Literal

from dotenv import load_dotenv
load_dotenv()

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

import ai_provider
import prompt_builder

DATABASE_URL = "sqlite:///./briefnote.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, default="Untitled")
    content = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class DocumentSummary(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentCreate(BaseModel):
    title: str | None = None
    content: str | None = None


class DocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AiChatRequest(BaseModel):
    document_id: str
    selection: str | None = None
    action: Literal["ask", "summarize", "rewrite", "extract"]
    user_message: str
    model: str | None = None


class AiSettings(BaseModel):
    model: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/api/documents", response_model=list[DocumentSummary])
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentModel).order_by(DocumentModel.updated_at.desc()).all()
    return [DocumentSummary.model_validate(doc) for doc in docs]


@app.post("/api/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(data: DocumentCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    doc = DocumentModel(
        id=str(uuid.uuid4()),
        title=data.title or "Untitled",
        content=data.content or "",
        created_at=now,
        updated_at=now,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return DocumentResponse.model_validate(doc)


@app.get("/api/documents/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse.model_validate(doc)


@app.put("/api/documents/{doc_id}", response_model=DocumentResponse)
def update_document(doc_id: str, data: DocumentUpdate, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if data.title is not None:
        doc.title = data.title
    if data.content is not None:
        doc.content = data.content
    doc.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(doc)
    return DocumentResponse.model_validate(doc)


@app.delete("/api/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()


@app.get("/api/ai/settings", response_model=AiSettings)
def get_ai_settings():
    import ai_provider
    return AiSettings(model=ai_provider.DEFAULT_MODEL)


@app.post("/api/ai/chat")
async def ai_chat(request: AiChatRequest, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == request.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    messages = prompt_builder.build_messages(
        document_content=doc.content,
        action=request.action,
        user_message=request.user_message,
        selection=request.selection,
        title=doc.title,
    )

    async def stream():
        try:
            for chunk in ai_provider.stream_chat(messages, model=request.model):
                yield json.dumps({"delta": chunk}) + "\n"
            yield "[DONE]\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
            yield "[DONE]\n"

    return StreamingResponse(stream(), media_type="application/x-ndjson")
