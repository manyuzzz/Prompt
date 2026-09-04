import { useState, useEffect, useRef } from 'react'
import { chatAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { timeAgo } from '../utils/helpers'
import { Send, Plus, Trash2, MessageSquare, Sparkles, Bot, User } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function Chat() {
  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const messagesEnd = useRef(null)
  const toast = useToast()

  useEffect(() => {
    loadConversations()
    chatAPI.getSuggestions().then(r => setSuggestions(r.data.suggestions || [])).catch(() => {})
  }, [])

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadConversations = async () => {
    try {
      const { data } = await chatAPI.getConversations()
      setConversations(data.conversations || [])
    } catch { }
  }

  const loadConversation = async (id) => {
    try {
      const { data } = await chatAPI.getConversation(id)
      setMessages(data.messages || [])
      setActiveId(id)
    } catch { toast.error('Failed to load conversation') }
  }

  const newChat = () => {
    setActiveId(null)
    setMessages([])
  }

  const sendMessage = async (text = input.trim()) => {
    if (!text || sending) return
    setInput('')
    setSending(true)
    const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() }
    setMessages(prev => [...prev, userMsg])

    try {
      const { data } = await chatAPI.send({ message: text, conversation_id: activeId })
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply, timestamp: new Date().toISOString() }])
      if (!activeId && data.conversation_id) {
        setActiveId(data.conversation_id)
        loadConversations()
      }
    } catch { toast.error('Failed to send message') }
    finally { setSending(false) }
  }

  const deleteConversation = async (id, e) => {
    e.stopPropagation()
    try {
      await chatAPI.deleteConversation(id)
      setConversations(prev => prev.filter(c => c.id !== id))
      if (activeId === id) newChat()
    } catch { toast.error('Failed to delete') }
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4 animate-fade-in">
      {/* Sidebar */}
      <div className="w-64 flex flex-col gap-2 shrink-0">
        <button onClick={newChat} className="btn-secondary flex items-center gap-2 justify-center">
          <Plus size={16} /> New Chat
        </button>
        <div className="flex-1 overflow-y-auto space-y-1">
          {conversations.map(c => (
            <button key={c.id}
              onClick={() => loadConversation(c.id)}
              className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors group flex items-start gap-2 ${activeId === c.id ? 'bg-primary-600/20 text-primary-300 border border-primary-600/30' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
            >
              <MessageSquare size={14} className="mt-0.5 shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="truncate font-medium">{c.title || 'New conversation'}</div>
                <div className="text-xs text-gray-600">{timeAgo(c.updated_at)}</div>
              </div>
              <button onClick={(e) => deleteConversation(c.id, e)}
                className="opacity-0 group-hover:opacity-100 text-gray-600 hover:text-red-400 p-0.5 transition-all">
                <Trash2 size={12} />
              </button>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col card p-0 overflow-hidden">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 rounded-2xl bg-primary-600/10 border border-primary-600/30 flex items-center justify-center mb-4">
                <Sparkles size={28} className="text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">AI Placement Assistant</h3>
              <p className="text-gray-400 max-w-md mb-8">Ask me anything about placements — DSA, system design, HR questions, resume tips, company strategies, and more.</p>
              <div className="grid grid-cols-2 gap-2 max-w-lg w-full">
                {suggestions.slice(0, 4).map((s, i) => (
                  <button key={i} onClick={() => sendMessage(s)}
                    className="text-left text-sm px-3 py-2.5 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 transition-colors">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-primary-600' : 'bg-gray-700'}`}>
                {msg.role === 'user' ? <User size={14} className="text-white" /> : <Bot size={14} className="text-primary-400" />}
              </div>
              <div className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm ${msg.role === 'user' ? 'bg-primary-600 text-white rounded-tr-sm' : 'bg-gray-800 text-gray-100 rounded-tl-sm'}`}>
                {msg.role === 'assistant' ? (
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                ) : msg.content}
              </div>
            </div>
          ))}

          {sending && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                <Bot size={14} className="text-primary-400" />
              </div>
              <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3">
                <div className="flex gap-1.5">
                  {[0, 1, 2].map(i => (
                    <div key={i} className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                  ))}
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEnd} />
        </div>

        <div className="border-t border-gray-800 p-4">
          <div className="flex gap-3">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder="Ask about placements, DSA, interviews..."
              className="input flex-1"
            />
            <button onClick={() => sendMessage()} disabled={!input.trim() || sending}
              className="btn-primary px-4">
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
