import { useCallback, useEffect, useRef, useState } from 'react'
import { sendMessage, fetchMessages, fetchLead } from '../services/api'
import type { Message, Lead } from '../types/chat'
import './App.css'

const WELCOME: Message = {
  id: 'welcome',
  conversation_id: '',
  sender_type: 'BOT',
  content:
    "Hi! I'm the PrimeHomes Realty assistant. Tell me what you're looking for — for example: a 3-bedroom apartment in Lekki around ₦80 million.",
  status: 'PROCESSED',
  created_at: new Date().toISOString(),
}

function classificationColor(c: string | null | undefined) {
  if (!c) return ''
  if (c === 'HOT') return 'badge-hot'
  if (c === 'WARM') return 'badge-warm'
  if (c === 'COLD') return 'badge-cold'
  return 'badge-unqualified'
}

function formatBudget(lead: Lead) {
  if (lead.budget_max == null) return null
  const n = lead.budget_max
  if (n >= 1_000_000) return `₦${(n / 1_000_000).toFixed(n % 1_000_000 === 0 ? 0 : 1)}M`
  return `₦${n.toLocaleString()}`
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([WELCOME])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [leadId, setLeadId] = useState<string | null>(null)
  const [lead, setLead] = useState<Lead | null>(null)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const pollRef = useRef<number | null>(null)

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, processing])

  const stopPolling = () => {
    if (pollRef.current) {
      window.clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  const startPolling = useCallback((convId: string, lid: string) => {
    stopPolling()
    let attempts = 0
    pollRef.current = window.setInterval(async () => {
      attempts += 1
      try {
        const msgs = await fetchMessages(convId)
        setMessages((prev) => {
          const welcome = prev.find((m) => m.id === 'welcome')
          return welcome ? [welcome, ...msgs] : msgs
        })
        const hasBot = msgs.some((m) => m.sender_type === 'BOT')
        if (hasBot) {
          setProcessing(false)
          stopPolling()
        }
        const updatedLead = await fetchLead(lid)
        setLead(updatedLead)
      } catch {
        /* ignore transient poll errors */
      }
      if (attempts > 40) {
        setProcessing(false)
        stopPolling()
      }
    }, 1500)
  }, [])

  useEffect(() => () => stopPolling(), [])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || sending) return

    setError(null)
    setSending(true)
    setInput('')

    const optimistic: Message = {
      id: `temp-${Date.now()}`,
      conversation_id: conversationId || '',
      sender_type: 'CUSTOMER',
      content: text,
      status: 'RECEIVED',
      created_at: new Date().toISOString(),
    }
    setMessages((m) => [...m, optimistic])

    try {
      const res = await sendMessage({
        content: text,
        conversation_id: conversationId,
        lead_id: leadId,
      })

      setConversationId(res.conversation_id)
      setLeadId(res.lead_id)
      if (res.lead) setLead(res.lead)

      setMessages((prev) => {
        const withoutTemp = prev.filter((m) => m.id !== optimistic.id)
        const next = [...withoutTemp, res.customer_message]
        if (res.bot_message) next.push(res.bot_message)
        return next
      })

      if (res.processing) {
        setProcessing(true)
        startPolling(res.conversation_id, res.lead_id)
      } else {
        setProcessing(false)
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong')
      setMessages((prev) => prev.filter((m) => m.id !== optimistic.id))
    } finally {
      setSending(false)
    }
  }

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="shell">
      <header className="header">
        <div className="brand">
          <div className="logo">PH</div>
          <div>
            <h1>PrimeHomes Realty</h1>
            <p className="tagline">Lead Assistant</p>
          </div>
        </div>
        {lead?.classification && (
          <span className={`badge ${classificationColor(lead.classification)}`}>
            {lead.classification}
            {lead.score != null ? ` · ${lead.score}` : ''}
          </span>
        )}
      </header>

      <main className="layout">
        <section className="chat-panel">
          <div className="messages">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`bubble-row ${m.sender_type === 'CUSTOMER' ? 'right' : 'left'}`}
              >
                {m.sender_type !== 'CUSTOMER' && <div className="avatar bot">AI</div>}
                <div className={`bubble ${m.sender_type === 'CUSTOMER' ? 'customer' : 'bot'}`}>
                  {m.content}
                </div>
              </div>
            ))}
            {processing && (
              <div className="bubble-row left">
                <div className="avatar bot">AI</div>
                <div className="bubble bot typing">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {error && <div className="error-bar">{error}</div>}

          <div className="composer">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Describe what you're looking for..."
              rows={1}
              disabled={sending}
            />
            <button
              type="button"
              className="send-btn"
              onClick={handleSend}
              disabled={sending || !input.trim()}
              aria-label="Send"
            >
              {sending ? '…' : 'Send'}
            </button>
          </div>
        </section>

        <aside className="side-panel">
          <h2>Lead summary</h2>
          {!lead ? (
            <p className="muted">Start chatting and details will appear here.</p>
          ) : (
            <dl className="lead-grid">
              <div>
                <dt>Status</dt>
                <dd>{lead.status}</dd>
              </div>
              <div>
                <dt>Intent</dt>
                <dd>{lead.intent || lead.transaction_type || '—'}</dd>
              </div>
              <div>
                <dt>Property</dt>
                <dd>
                  {lead.property_type || '—'}
                  {lead.bedrooms != null ? ` · ${lead.bedrooms} bed` : ''}
                </dd>
              </div>
              <div>
                <dt>Location</dt>
                <dd>{lead.location || '—'}</dd>
              </div>
              <div>
                <dt>Budget</dt>
                <dd>{formatBudget(lead) || '—'}</dd>
              </div>
              <div>
                <dt>Timeline</dt>
                <dd>{lead.timeline || '—'}</dd>
              </div>
              <div>
                <dt>Score</dt>
                <dd>{lead.score != null ? lead.score : '—'}</dd>
              </div>
              <div>
                <dt>Class</dt>
                <dd>
                  {lead.classification ? (
                    <span className={`badge ${classificationColor(lead.classification)}`}>
                      {lead.classification}
                    </span>
                  ) : (
                    '—'
                  )}
                </dd>
              </div>
            </dl>
          )}

          <div className="hint">
            <strong>Tip for n8n</strong>
            <p>
              Point your webhook to path <code>lead-process-message</code>. After AI extraction, POST
              updates to <code>/api/v1/internal/leads/&#123;id&#125;</code> and bot replies to{' '}
              <code>/api/v1/internal/bot-reply</code>.
            </p>
          </div>
        </aside>
      </main>
    </div>
  )
}
