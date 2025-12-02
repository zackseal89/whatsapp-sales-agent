'use client'

import { useState, useEffect, useRef } from 'react'
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Phone, Video, MoreVertical } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { createClient } from '@/lib/supabase/client'

interface Message {
  id: string
  message_text: string
  direction: 'inbound' | 'outbound'
  created_at: string
  sender_type: string
  is_automated: boolean
}

interface ChatInterfaceProps {
  conversationId: string
  initialMessages: Message[]
  customerName: string
  customerPhone: string
}

export function ChatInterface({ 
  conversationId, 
  initialMessages,
  customerName,
  customerPhone
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages)
  const [newMessage, setNewMessage] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)
  const supabase = createClient()

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  // Subscribe to new messages
  useEffect(() => {
    const channel = supabase
      .channel(`conversation:${conversationId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `conversation_id=eq.${conversationId}`
        },
        (payload) => {
          setMessages((current) => [...current, payload.new as Message])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [conversationId, supabase])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim()) return

    // Optimistic update
    const tempMessage: Message = {
      id: crypto.randomUUID(),
      message_text: newMessage,
      direction: 'outbound',
      created_at: new Date().toISOString(),
      sender_type: 'agent',
      is_automated: false
    }
    
    setMessages(prev => [...prev, tempMessage])
    setNewMessage('')

    // TODO: Implement actual send logic via API/Server Action
    console.log('Sending message:', newMessage)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] bg-white rounded-lg border shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-3">
          <Avatar>
            <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${customerName}`} />
            <AvatarFallback>{customerName.substring(0, 2).toUpperCase()}</AvatarFallback>
          </Avatar>
          <div>
            <h3 className="font-semibold">{customerName}</h3>
            <p className="text-sm text-muted-foreground">{customerPhone}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Phone className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Video className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <MoreVertical className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Messages Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50"
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.direction === 'outbound' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                message.direction === 'outbound'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-white border shadow-sm'
              }`}
            >
              <p className="text-sm">{message.message_text}</p>
              <div className={`text-xs mt-1 ${
                message.direction === 'outbound' 
                  ? 'text-primary-foreground/70' 
                  : 'text-muted-foreground'
              }`}>
                {formatDistanceToNow(new Date(message.created_at), { addSuffix: true })}
                {message.is_automated && ' • Automated'}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t bg-white">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <Input
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type a message..."
            className="flex-1"
          />
          <Button type="submit">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}
