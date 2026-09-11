import type { ChatResponse, Message, Lead } from '../types/chat'

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1'

export async function sendMessage(payload: {
  content: string
  conversation_id?: string | null
  lead_id?: string | null
  name?: string
  email?: string
  phone?: string
}): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to send message')
  }
  return res.json()
}

export async function fetchMessages(conversationId: string): Promise<Message[]> {
  const res = await fetch(`${API_BASE}/conversations/${conversationId}/messages`)
  if (!res.ok) throw new Error('Failed to load messages')
  return res.json()
}

export async function fetchLead(leadId: string): Promise<Lead> {
  const res = await fetch(`${API_BASE}/leads/${leadId}`)
  if (!res.ok) throw new Error('Failed to load lead')
  return res.json()
}
