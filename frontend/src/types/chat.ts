export interface Message {
  id: string
  conversation_id: string
  sender_type: 'CUSTOMER' | 'BOT' | 'AGENT'
  content: string
  status: string
  created_at: string
}

export interface Lead {
  id: string
  name: string | null
  email: string | null
  phone: string | null
  intent: string | null
  property_type: string | null
  bedrooms: number | null
  location: string | null
  budget_max: number | null
  currency: string | null
  timeline: string | null
  status: string
  score: number | null
  classification: string | null
}

export interface ChatResponse {
  conversation_id: string
  lead_id: string
  customer_message: Message
  bot_message: Message | null
  lead: Lead | null
  processing: boolean
}
