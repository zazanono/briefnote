import { useEffect, useRef, useState } from 'react'
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { AiChatRequest, Document, DocumentSummary } from './types'
import { createDocument, deleteDocument, getDocument, listDocuments, updateDocument } from './api'

function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

function DocItem({
  doc,
  isActive,
  onSelect,
  onRename,
  onDelete,
}: {
  doc: DocumentSummary
  isActive: boolean
  onSelect: () => void
  onRename: (title: string) => void
  onDelete: () => void
}) {
  const [editing, setEditing] = useState(false)
  const [value, setValue] = useState(doc.title)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (editing) inputRef.current?.select()
  }, [editing])

  function handleBlur() {
    setEditing(false)
    if (value.trim() && value !== doc.title) onRename(value.trim())
    else setValue(doc.title)
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter') inputRef.current?.blur()
    if (e.key === 'Escape') {
      setValue(doc.title)
      setEditing(false)
    }
  }

  return (
    <div className={`doc-item ${isActive ? 'active' : ''}`} onClick={onSelect}>
      <div className="doc-item-title">
        {editing ? (
          <input
            ref={inputRef}
            className="rename-input"
            value={value}
            onChange={e => setValue(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            onClick={e => e.stopPropagation()}
          />
        ) : (
          <>
            <span>{doc.title || 'Untitled'}</span>
            <div className="doc-item-actions">
              <button
                className="icon-btn"
                onClick={e => {
                  e.stopPropagation()
                  setEditing(true)
                }}
              >
                rename
              </button>
              <button
                className="icon-btn delete"
                onClick={e => {
                  e.stopPropagation()
                  if (window.confirm(`Delete "${doc.title}"?`)) onDelete()
                }}
              >
                del
              </button>
            </div>
          </>
        )}
      </div>
      <div className="doc-item-date">{formatDate(doc.updated_at)}</div>
    </div>
  )
}

function Sidebar({
  docs,
  currentId,
  onSelect,
  onCreate,
  onRename,
  onDelete,
}: {
  docs: DocumentSummary[]
  currentId: string | null
  onSelect: (id: string) => void
  onCreate: () => void
  onRename: (id: string, title: string) => void
  onDelete: (id: string) => void
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Documents</h2>
      </div>
      <div className="doc-list">
        {docs.map(doc => (
          <DocItem
            key={doc.id}
            doc={doc}
            isActive={doc.id === currentId}
            onSelect={() => onSelect(doc.id)}
            onRename={title => onRename(doc.id, title)}
            onDelete={() => onDelete(doc.id)}
          />
        ))}
        {docs.length === 0 && (
          <div className="empty-state">
            <p>No documents yet</p>
          </div>
        )}
      </div>
      <div style={{ padding: '8px' }}>
        <button className="new-doc-btn" onClick={onCreate}>
          + New Document
        </button>
      </div>
    </div>
  )
}

function EditorPane({
  doc,
  onContentChange,
  onTitleChange,
  saveState,
}: {
  doc: Document | null
  onContentChange: (html: string) => void
  onTitleChange: (title: string) => void
  saveState: 'saved' | 'saving' | 'unsaved'
}) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: doc?.content || '',
    onUpdate: ({ editor }) => {
      onContentChange(editor.getHTML())
    },
  })

  const [title, setTitle] = useState(doc?.title || '')

  useEffect(() => {
    if (doc) {
      editor?.commands.setContent(doc.content || '', false)
      setTitle(doc.title)
    }
  }, [doc?.id])

  function handleTitleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setTitle(e.target.value)
    onTitleChange(e.target.value)
  }

  if (!doc) {
    return (
      <div className="editor-pane">
        <div className="empty-state">
          <p>Select a document or create a new one</p>
        </div>
      </div>
    )
  }

  return (
    <div className="editor-pane">
      <div className="editor-header">
        <input
          className="editor-title-input"
          value={title}
          onChange={handleTitleChange}
          placeholder="Untitled"
        />
      </div>
      <div className="editor-content">
        <EditorContent editor={editor} />
      </div>
      <div className="save-indicator">
        {saveState === 'saving' ? 'Saving...' : saveState === 'unsaved' ? 'Unsaved changes' : 'Saved'}
      </div>
    </div>
  )
}

function AiPanel({ documentContent }: { documentContent: string }) {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleAction(action: 'ask' | 'summarize' | 'rewrite' | 'extract') {
    setLoading(true)
    setResponse(null)
    try {
      const body: AiChatRequest = {
        document_content: documentContent,
        selection: null,
        action,
        user_message: action === 'ask' ? message : '',
      }
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await res.json()
      setResponse(data.message || 'AI response')
    } catch {
      setResponse('Error: Could not reach AI endpoint')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="ai-panel">
      <div className="ai-header">
        <h3>AI Assistant</h3>
        <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
          Using: full document
        </p>
      </div>
      <div className="ai-messages">
        {response && <div className="ai-message">{response}</div>}
        {!response && (
          <div className="empty-state">
            <p>Ask questions about your document, or use an action below</p>
          </div>
        )}
      </div>
      <div className="ai-actions">
        <div className="action-buttons">
          <button className="action-btn" onClick={() => handleAction('summarize')} disabled={loading}>
            Summarize
          </button>
          <button className="action-btn" onClick={() => handleAction('rewrite')} disabled={loading}>
            Rewrite
          </button>
          <button className="action-btn" onClick={() => handleAction('extract')} disabled={loading}>
            Extract
          </button>
        </div>
        <textarea
          className="ai-input"
          rows={2}
          placeholder="Ask a question..."
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        <button
          className="ai-submit"
          onClick={() => handleAction('ask')}
          disabled={loading || !message.trim()}
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>
    </div>
  )
}

export default function App() {
  const [docs, setDocs] = useState<DocumentSummary[]>([])
  const [currentDoc, setCurrentDoc] = useState<Document | null>(null)
  const [saveState, setSaveState] = useState<'saved' | 'saving' | 'unsaved'>('saved')
  const saveTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const pendingContent = useRef<string | null>(null)
  const pendingTitle = useRef<string | null>(null)

  async function loadDocs() {
    try {
      const list = await listDocuments()
      setDocs(list)
    } catch (err) {
      console.error('Failed to load docs:', err)
    }
  }

  async function loadDoc(id: string) {
    try {
      const doc = await getDocument(id)
      setCurrentDoc(doc)
      setSaveState('saved')
    } catch (err) {
      console.error('Failed to load doc:', err)
    }
  }

  useEffect(() => {
    loadDocs()
  }, [])

  function scheduleSave() {
    if (saveTimer.current) clearTimeout(saveTimer.current)
    setSaveState('unsaved')
    saveTimer.current = setTimeout(async () => {
      if (!currentDoc) return
      setSaveState('saving')
      try {
        const doc = await updateDocument(currentDoc.id, pendingTitle.current ?? undefined, pendingContent.current ?? undefined)
        setCurrentDoc(doc)
        setSaveState('saved')
        pendingContent.current = null
        pendingTitle.current = null
        loadDocs()
      } catch (err) {
        console.error('Save failed:', err)
        setSaveState('unsaved')
      }
    }, 500)
  }

  function handleContentChange(html: string) {
    if (!currentDoc) return
    pendingContent.current = html
    scheduleSave()
  }

  function handleTitleChange(title: string) {
    if (!currentDoc) return
    pendingTitle.current = title
    setCurrentDoc(prev => prev ? { ...prev, title } : null)
    scheduleSave()
  }

  async function handleCreate() {
    try {
      const doc = await createDocument()
      await loadDocs()
      setCurrentDoc(doc)
    } catch (err) {
      console.error('Failed to create doc:', err)
    }
  }

  async function handleDelete(id: string) {
    try {
      await deleteDocument(id)
      if (currentDoc?.id === id) setCurrentDoc(null)
      await loadDocs()
    } catch (err) {
      console.error('Failed to delete doc:', err)
    }
  }

  async function handleRename(id: string, title: string) {
    try {
      const doc = await updateDocument(id, title)
      await loadDocs()
      if (currentDoc?.id === id) setCurrentDoc(doc)
    } catch (err) {
      console.error('Failed to rename doc:', err)
    }
  }

  return (
    <div className="app">
      <Sidebar
        docs={docs}
        currentId={currentDoc?.id ?? null}
        onSelect={loadDoc}
        onCreate={handleCreate}
        onRename={handleRename}
        onDelete={handleDelete}
      />
      <EditorPane
        doc={currentDoc}
        onContentChange={handleContentChange}
        onTitleChange={handleTitleChange}
        saveState={saveState}
      />
      <AiPanel documentContent={currentDoc?.content || ''} />
    </div>
  )
}
