import { useEffect, useRef, useState } from 'react'
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { AiAction, AiChatRequest, AiSettings, Document, DocumentSummary } from './types'
import { createDocument, deleteDocument, getAiSettings, getDocument, listDocuments, updateDocument, getChatHistory } from './api'

function DocItem({
  doc,
  isActive,
  onSelect,
  onDeleteClick,
}: {
  doc: DocumentSummary
  isActive: boolean
  onSelect: () => void
  onDeleteClick: (doc: DocumentSummary) => void
}) {
  function handleDeleteClick(e: React.MouseEvent) {
    e.stopPropagation()
    e.preventDefault()
    onDeleteClick(doc)
  }

  return (
    <div className={`doc-item ${isActive ? 'active' : ''}`} onClick={onSelect}>
      <div className="doc-item-title">
        {doc.title || 'Untitled'}
      </div>
      <div className="doc-item-actions">
        <button
          className="icon-btn delete"
          onClick={handleDeleteClick}
          title="Delete"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
      </div>
    </div>
  )
}

function Sidebar({
  docs,
  loading,
  currentId,
  onSelect,
  onCreate,
  onDelete,
}: {
  docs: DocumentSummary[]
  loading: boolean
  currentId: string | null
  onSelect: (id: string) => void
  onCreate: () => void
  onDelete: (id: string) => void
}) {
  const [docToDelete, setDocToDelete] = useState<DocumentSummary | null>(null)

  useEffect(() => {
    if (!docToDelete) return
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
        e.preventDefault()
        onDelete(docToDelete.id)
        setDocToDelete(null)
      } else if (e.key === 'Escape') {
        e.preventDefault()
        setDocToDelete(null)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [docToDelete, onDelete])

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <button className="new-doc-btn" onClick={onCreate}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          New Document
        </button>
      </div>
      <div className="doc-list">
        {loading && docs.length === 0 && <div className="empty-state"><p>Loading...</p></div>}
        {docs.map(doc => (
          <DocItem
            key={doc.id}
            doc={doc}
            isActive={doc.id === currentId}
            onSelect={() => onSelect(doc.id)}
            onDeleteClick={setDocToDelete}
          />
        ))}
        {!loading && docs.length === 0 && (
          <div className="empty-state" style={{ padding: '24px 12px' }}>
            <p>No documents yet</p>
          </div>
        )}
      </div>

      {docToDelete && (
        <div className="modal-overlay" onClick={() => setDocToDelete(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-title">Delete Document</div>
            <div className="modal-body">
              Are you sure you want to delete "{docToDelete.title || 'Untitled'}"? This action cannot be undone.
            </div>
            <div className="modal-actions">
              <button className="modal-btn cancel" onClick={() => setDocToDelete(null)}>Cancel</button>
              <button className="modal-btn delete" onClick={() => {
                onDelete(docToDelete.id)
                setDocToDelete(null)
              }}>
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function EditorPane({
  doc,
  editor,
  onTitleChange,
  onTitleBlur,
  saveState,
}: {
  doc: Document | null
  editor: ReturnType<typeof useEditor>
  onTitleChange: (title: string) => void
  onTitleBlur: (title: string, getHtml: () => string) => void
  saveState: 'saved' | 'saving' | 'unsaved'
}) {
  const [title, setTitle] = useState(doc?.title || '')
  const [editingTitle, setEditingTitle] = useState(false)
  const renameInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (doc && !editingTitle) setTitle(doc.title)
  }, [doc?.id, doc?.title, editingTitle])

  function handleTitleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setTitle(e.target.value)
    onTitleChange(e.target.value)
  }

  function handleTitleBlur() {
    setEditingTitle(false)
    onTitleBlur(title, () => editor?.getHTML() ?? '')
  }

  function handleTitleFocus() {
    setEditingTitle(true)
  }

  if (!doc) {
    return (
      <div className="editor-pane" style={{ justifyContent: 'center', alignItems: 'center' }}>
        <div className="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--border)" strokeWidth="1" style={{ marginBottom: 16 }}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          <p>Select a document or create a new one</p>
        </div>
      </div>
    )
  }

  return (
    <div className="editor-pane">
      <div className="editor-scroll-area">
        <div className="document-page">
          <div className="editor-header">
            <div className="editor-title-row">
              <input
                ref={renameInputRef as React.RefObject<HTMLInputElement>}
                className="editor-title-input"
                value={title}
                onChange={handleTitleChange}
                onBlur={handleTitleBlur}
                onFocus={handleTitleFocus}
                placeholder="Untitled"
              />
              <button
                className="icon-btn rename-btn"
                onClick={() => renameInputRef.current?.focus()}
                title="Rename"
                style={{ opacity: 0, transition: 'opacity 0.15s' }}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
              </button>
            </div>
            <div className="save-indicator" data-state={saveState}>
              {saveState === 'saving' ? 'Saving...' : saveState === 'unsaved' ? 'Unsaved' : 'Saved'}
            </div>
          </div>
          <div className="editor-content">
            <EditorContent editor={editor} />
          </div>
        </div>
      </div>
    </div>
  )
}

function AiPanel({
  documentId,
  editor,
  lastSelectionRef,
  className,
}: {
  documentId: string | null
  editor: ReturnType<typeof useEditor>
  lastSelectionRef: React.RefObject<{ from: number; to: number } | null>
  className?: string
}) {
  const [message, setMessage] = useState('')
  const [chatMessages, setChatMessages] = useState<import('./types').ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [settings, setSettings] = useState<AiSettings | null>(null)
  const [showSettings, setShowSettings] = useState(false)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const abortRef = useRef<AbortController | null>(null)
  const lastRequestRef = useRef<{ action: AiAction; message: string; selection: string | null } | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    getAiSettings().then(setSettings).catch(() => {})
  }, [])

  useEffect(() => {
    setChatMessages([])
    setError(null)
    setLoading(false)
    if (documentId) {
      getChatHistory(documentId).then(setChatMessages).catch(() => {})
    }
  }, [documentId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  function getSelection(): string | null {
    if (!editor) return null
    const stored = lastSelectionRef.current
    if (stored && stored.from !== stored.to) {
      return editor.state.doc.textBetween(stored.from, stored.to, ' ')
    }
    const { from, to } = editor.state.selection
    if (from === to) return null
    return editor.state.doc.textBetween(from, to, ' ')
  }

  function textToHtml(text: string): string {
    return text.split('\n\n').filter(p => p.trim()).map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('')
  }

  async function streamResponse(action: AiAction, overrideMessage?: string) {
    if (!documentId) return

    if (abortRef.current) {
      abortRef.current.abort()
    }
    abortRef.current = new AbortController()

    setLoading(true)
    setError(null)

    const sel = getSelection()
    let msg = action === 'ask' ? (overrideMessage ?? message) : ''
    if (action !== 'ask') {
      const target = sel ? 'selection' : 'document'
      if (action === 'summarize') msg = `Summarize ${target}`
      else if (action === 'rewrite') msg = `Rewrite ${target}`
      else if (action === 'extract') msg = `Extract information from ${target}`
    }

    lastRequestRef.current = { action, message: msg, selection: sel }

    const body: AiChatRequest = {
      document_id: documentId,
      selection: sel,
      action,
      user_message: msg,
      model: settings?.model,
    }

    const tempId = Date.now().toString()
    if (msg) {
      setChatMessages(prev => [...prev, {
        id: `user-${tempId}`,
        document_id: documentId,
        role: 'user',
        content: msg,
        created_at: new Date().toISOString()
      }])
    }

    const astId = `ast-${tempId}`
    setChatMessages(prev => [...prev, {
      id: astId,
      document_id: documentId,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString()
    }])

    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: abortRef.current.signal,
      })

      if (!res.body) throw new Error('No response body')
      const reader = res.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const text = decoder.decode(value)
        const lines = text.split('\n')
        for (const line of lines) {
          if (!line.trim() || line === '[DONE]') continue
          if (line.startsWith('{"error":')) {
            const err = JSON.parse(line)
            setError(err.error)
            continue
          }
          if (line.startsWith('{"delta":')) {
            try {
              const chunk = JSON.parse(line)
              setChatMessages(prev => prev.map(m => 
                m.id === astId ? { ...m, content: m.content + chunk.delta } : m
              ))
            } catch {
              continue
            }
          }
        }
      }
      
      if (!abortRef.current?.signal.aborted) {
        const history = await getChatHistory(documentId)
        setChatMessages(history)
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name === 'AbortError') {
        setError('Cancelled')
      } else {
        setError('Failed to reach AI endpoint')
      }
    } finally {
      setLoading(false)
      abortRef.current = null
    }
  }

  function handleAction(action: AiAction) {
    const msg = action === 'ask' ? message : ''
    setMessage('')
    streamResponse(action, msg)
  }

  function handleRegenerate() {
    if (!lastRequestRef.current) return
    const req = lastRequestRef.current
    if (req.action === 'ask') setMessage(req.message)
    streamResponse(req.action, req.message)
  }

  function handleCancel() {
    abortRef.current?.abort()
  }

  function handleCopy(content: string, id: string) {
    navigator.clipboard.writeText(content)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1500)
  }

  function handleInsert(content: string) {
    if (!editor || !content) return
    const html = textToHtml(content)
    editor.commands.insertContent(html)
  }

  function handleReplace(content: string) {
    if (!editor || !content) return
    const { from, to } = editor.state.selection
    if (from === to) {
      handleInsert(content)
    } else {
      const html = textToHtml(content)
      editor.commands.deleteRange({ from, to })
      editor.commands.insertContent(html)
    }
  }

  const hasSelection = (() => {
    const stored = lastSelectionRef.current
    if (stored && stored.from !== stored.to) return true
    if (!editor) return false
    return editor.state.selection.from !== editor.state.selection.to
  })()

  return (
    <div className={className || 'ai-panel'}>
      <div className="ai-header">
        <div className="ai-header-row">
          <div className="ai-header-title">
            <h3>Assistant</h3>
            <span className="ai-context-badge">{hasSelection ? 'Selection' : 'Document'}</span>
          </div>
          <button className="icon-btn" onClick={() => setShowSettings(s => !s)} onMouseDown={e => e.preventDefault()} title="Settings">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          </button>
        </div>
        {showSettings && (
          <div className="ai-settings">
            <label className="settings-label">Model</label>
            <input
              className="settings-input"
              value={settings?.model || ''}
              onChange={e => setSettings(s => s ? { ...s, model: e.target.value } : { model: e.target.value })}
              placeholder="openrouter/free"
              onMouseDown={e => e.stopPropagation()}
            />
          </div>
        )}
      </div>

      <div className="ai-messages">
        {chatMessages.length === 0 && !loading && !error && (
          <div className="empty-state">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-light)" strokeWidth="1.5" style={{ marginBottom: 12 }}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            <p>Ask about your document, or use an action below.</p>
          </div>
        )}
        
        {chatMessages.map((m, index) => (
          <div key={m.id} className={`ai-message-bubble ${m.role}`}>
            <div className="ai-message">{m.content || (m.role === 'assistant' && loading ? 'Thinking...' : '')}</div>
            {m.role === 'assistant' && m.content && (
              <div className="ai-response-actions">
                <button className="action-btn small" onClick={() => handleCopy(m.content, m.id)}>
                  {copiedId === m.id ? 'Copied!' : 'Copy'}
                </button>
                <button className="action-btn small" onClick={() => handleInsert(m.content)}>Insert</button>
                <button className="action-btn small" onClick={() => handleReplace(m.content)}>Replace</button>
                {index === chatMessages.length - 1 && (
                  <button className="action-btn small" onClick={handleRegenerate}>Retry</button>
                )}
              </div>
            )}
          </div>
        ))}
        
        {error && (
          <div className="ai-message error">{error}</div>
        )}
        {loading && !chatMessages.some(m => m.id.startsWith('ast-')) && (
          <div className="ai-message loading">
            Thinking...
            <button className="cancel-btn" onClick={handleCancel}>Cancel</button>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="ai-actions">
        <div className="action-buttons">
          <button className="action-btn" onClick={() => handleAction('summarize')} onMouseDown={e => e.preventDefault()} disabled={loading || !documentId}>
            Summarize
          </button>
          <button className="action-btn" onClick={() => handleAction('rewrite')} onMouseDown={e => e.preventDefault()} disabled={loading || !documentId}>
            Rewrite
          </button>
          <button className="action-btn" onClick={() => handleAction('extract')} onMouseDown={e => e.preventDefault()} disabled={loading || !documentId}>
            Extract
          </button>
        </div>
        <div className="ai-input-wrapper">
          <textarea
            className="ai-input"
            rows={1}
            placeholder="Ask a question..."
            value={message}
            onChange={e => setMessage(e.target.value)}
            disabled={loading}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                if (!loading && documentId && (message.trim() || hasSelection)) {
                  handleAction('ask')
                }
              }
            }}
          />
          <button
            className="ai-submit"
            onClick={() => handleAction('ask')}
            onMouseDown={e => e.preventDefault()}
            disabled={loading || !documentId || (!message.trim() && !hasSelection)}
            title="Send"
          >
            {loading ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path></svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [docs, setDocs] = useState<DocumentSummary[]>([])
  const [docsLoading, setDocsLoading] = useState(false)
  const [currentDoc, setCurrentDoc] = useState<Document | null>(null)
  const [saveState, setSaveState] = useState<'saved' | 'saving' | 'unsaved'>('saved')
  const [mobilePane, setMobilePane] = useState<'sidebar' | 'editor' | 'ai'>('editor')
  const saveTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const lastSelectionRef = useRef<{ from: number; to: number } | null>(null)
  const currentDocRef = useRef<Document | null>(currentDoc)
  
  // Keep ref in sync
  currentDocRef.current = currentDoc

  const editor = useEditor({
    extensions: [StarterKit],
    content: currentDoc?.content || '',
    onUpdate: ({ editor }) => {
      if (!currentDocRef.current) return
      const html = editor.getHTML()
      setCurrentDoc(prev => prev ? { ...prev, content: html } : null)
      scheduleSave(() => html)
    },
    onSelectionUpdate: ({ editor }) => {
      const { from, to } = editor.state.selection
      if (from !== to) {
        lastSelectionRef.current = { from, to }
      }
    },
  })

  useEffect(() => {
    if (!editor || !currentDoc) return
    const current = editor.getHTML()
    if (currentDoc.content !== undefined && current !== currentDoc.content) {
      editor.commands.setContent(currentDoc.content || '', false)
    }
    // Auto-focus when switching documents or creating a new one
    // Using setTimeout to ensure it happens after render
    setTimeout(() => {
      if (!editor.isDestroyed) {
        editor.commands.focus('end')
      }
    }, 0)
  }, [currentDoc?.id, editor])

  async function loadDocs() {
    // Prevent duplicate in-flight requests
    if (docsLoading) return
    
    setDocsLoading(true)
    try {
      const list = await listDocuments()
      // Sort by created_at descending to prevent shuffling
      const sorted = [...list].sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
      setDocs(sorted)
    } catch (err) {
      console.error('Failed to load docs:', err)
    } finally {
      setDocsLoading(false)
    }
  }

  async function loadDoc(id: string, prevDocId?: string, prevDocTitle?: string, getPrevHtml?: () => string) {
    if (saveTimer.current) {
      clearTimeout(saveTimer.current)
      saveTimer.current = null
    }

    // Save previous doc's content if we have context
    if (prevDocId && getPrevHtml) {
      const content = getPrevHtml()
      const isEmpty = content === '' || content === `<p>${prevDocTitle ?? ''}</p>`
      if (!isEmpty) {
        try {
          // Pass undefined for title so we don't overwrite a concurrent title change
          const updated = await updateDocument(prevDocId, undefined, content)
          // Update the docs array so the sidebar has the latest state for the old doc
          setDocs(prev => prev.map(d => d.id === updated.id ? updated : d))
        } catch (err) {
          console.error('Auto-save failed:', err)
        }
      }
    }

    // Then load new doc
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

  function scheduleSave(getHtml: () => string) {
    if (saveTimer.current) clearTimeout(saveTimer.current)
    
    const docId = currentDocRef.current?.id
    if (!docId) return
    
    setSaveState('unsaved')
    saveTimer.current = setTimeout(async () => {
      // Use the latest title when the timeout fires, but the html that was generated
      const latestDoc = currentDocRef.current
      if (!latestDoc || latestDoc.id !== docId) return
      
      setSaveState('saving')
      try {
        const content = getHtml()
        const doc = await updateDocument(docId, latestDoc.title, content)
        // Update docs array in place instead of refetching
        setDocs(prev => prev.map(d => d.id === doc.id ? doc : d))
        
        // Only update currentDoc if we haven't switched documents
        if (currentDocRef.current?.id === docId) {
          setCurrentDoc(doc)
          setSaveState('saved')
        }
      } catch (err) {
        console.error('Save failed:', err)
        if (currentDocRef.current?.id === docId) {
          setSaveState('unsaved')
        }
      }
    }, 500)
  }

  function handleTitleChange(title: string) {
    if (!currentDocRef.current) return
    setCurrentDoc(prev => prev ? { ...prev, title } : null)
    setDocs(prev => prev.map(d => d.id === currentDocRef.current?.id ? { ...d, title } : d))
  }

  async function handleTitleBlur(title: string, getHtml: () => string) {
    const doc = currentDocRef.current
    if (!doc) return
    const docId = doc.id
    const content = getHtml()
    setSaveState('saving')
    try {
      const updated = await updateDocument(docId, title, content)
      // Update docs array in place instead of refetching
      setDocs(prev => prev.map(d => d.id === updated.id ? updated : d))
      
      // Only update currentDoc if we haven't switched documents
      if (currentDocRef.current?.id === docId) {
        setCurrentDoc(updated)
        setSaveState('saved')
      }
    } catch (err) {
      console.error('Title save failed:', err)
      if (currentDocRef.current?.id === docId) {
        setSaveState('unsaved')
      }
    }
  }

  async function handleCreate() {
    try {
      const doc = await createDocument()
      setDocs(prev => [doc, ...prev])
      setCurrentDoc(doc)
      setSaveState('saved')
    } catch (err) {
      console.error('Failed to create doc:', err)
    }
  }

  async function handleDelete(id: string) {
    // Clear any pending save for this doc
    if (saveTimer.current) {
      clearTimeout(saveTimer.current)
      saveTimer.current = null
    }
    
    // Optimistic update for instant UI response
    setDocs(prev => prev.filter(d => d.id !== id))
    
    if (currentDoc?.id === id) {
      setCurrentDoc(null)
      setSaveState('saved')
    }
    
    try {
      await deleteDocument(id)
    } catch (err) {
      console.error('Failed to delete doc:', err)
      await loadDocs() // Revert on failure
    }
  }

  return (
    <div className="app">
      <div className="mobile-bar">
        <button
          className={mobilePane === 'sidebar' ? 'active' : ''}
          onClick={() => setMobilePane('sidebar')}
        >
          Docs
        </button>
        <button
          className={mobilePane === 'editor' ? 'active' : ''}
          onClick={() => setMobilePane('editor')}
        >
          Editor
        </button>
        <button
          className={mobilePane === 'ai' ? 'active' : ''}
          onClick={() => setMobilePane('ai')}
        >
          AI
        </button>
      </div>

      <div className={`pane-wrapper ${mobilePane === 'sidebar' ? 'mobile-active' : ''}`}>
        <Sidebar
          docs={docs}
          loading={docsLoading}
          currentId={currentDoc?.id ?? null}
          onSelect={id => {
            if (id === currentDoc?.id) {
              setMobilePane('editor')
              return
            }
            const prev = currentDoc
            loadDoc(
              id,
              prev ? prev.id : undefined,
              prev ? prev.title : undefined,
              () => editor?.getHTML() ?? ''
            )
            setMobilePane('editor')
          }}
          onCreate={() => { handleCreate(); setMobilePane('editor') }}
          onDelete={handleDelete}
        />
      </div>

      <div className={`pane-wrapper ${mobilePane === 'editor' ? 'mobile-active' : ''}`}>
        <EditorPane
          doc={currentDoc}
          editor={editor}
          onTitleChange={handleTitleChange}
          onTitleBlur={handleTitleBlur}
          saveState={saveState}
        />
      </div>

      <AiPanel
        documentId={currentDoc?.id ?? null}
        editor={editor}
        lastSelectionRef={lastSelectionRef}
        className={mobilePane === 'ai' ? 'ai-panel mobile-open' : undefined}
      />
    </div>
  )
}
