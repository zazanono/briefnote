export interface DocumentSummary {
  id: string
  title: string
  updated_at: string
}

export interface Document {
  id: string
  title: string
  content: string
  created_at: string
  updated_at: string
}

export interface AiChatRequest {
  document_content: string
  selection: string | null
  action: 'ask' | 'summarize' | 'rewrite' | 'extract'
  user_message: string
}
