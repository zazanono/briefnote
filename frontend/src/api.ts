import { AiSettings, ChatMessage, Document, DocumentSummary } from './types'

export async function listDocuments(): Promise<DocumentSummary[]> {
  const res = await fetch('/api/documents')
  if (!res.ok) throw new Error('Failed to list documents')
  return res.json()
}

export async function getDocument(id: string): Promise<Document> {
  const res = await fetch(`/api/documents/${id}`)
  if (!res.ok) throw new Error('Failed to get document')
  return res.json()
}

export async function createDocument(title?: string, content?: string): Promise<Document> {
  const res = await fetch('/api/documents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content }),
  })
  if (!res.ok) throw new Error('Failed to create document')
  return res.json()
}

export async function updateDocument(id: string, title?: string, content?: string): Promise<Document> {
  const res = await fetch(`/api/documents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content }),
  })
  if (!res.ok) throw new Error('Failed to update document')
  return res.json()
}

export async function deleteDocument(id: string): Promise<void> {
  const res = await fetch(`/api/documents/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete document')
}

export async function getAiSettings(): Promise<AiSettings> {
  const res = await fetch('/api/ai/settings')
  if (!res.ok) throw new Error('Failed to load AI settings')
  return res.json()
}

export async function getChatHistory(documentId: string): Promise<ChatMessage[]> {
  const res = await fetch(`/api/documents/${documentId}/chat?t=${Date.now()}`, {
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    }
  })
  if (!res.ok) throw new Error('Failed to load chat history')
  return res.json()
}
