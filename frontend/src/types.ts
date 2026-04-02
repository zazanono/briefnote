export interface DocumentSummary {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface Document {
  id: string
  title: string
  content: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: string
  document_id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export type AiAction = 'ask' | 'summarize' | 'rewrite' | 'extract'

export interface AiChatRequest {
  document_id: string
  selection: string | null
  action: AiAction
  user_message: string
  model?: string
}

export interface AiSettings {
  model: string
}
