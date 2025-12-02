import { createClient } from '@/lib/supabase/server'
import { notFound } from 'next/navigation'
import { ChatInterface } from '@/components/ChatInterface'

interface PageProps {
  params: Promise<{ id: string }>
}

export default async function ConversationPage({ params }: PageProps) {
  const { id } = await params
  const supabase = await createClient()

  // Fetch conversation details with customer info
  const { data: conversation } = await supabase
    .from('conversations')
    .select(`
      *,
      customer:customers(name, whatsapp_number)
    `)
    .eq('id', id)
    .single()

  if (!conversation) {
    notFound()
  }

  // Fetch messages
  const { data: messages } = await supabase
    .from('messages')
    .select('*')
    .eq('conversation_id', id)
    .order('created_at', { ascending: true })

  return (
    <div className="h-full">
      <div className="mb-4">
        <h2 className="text-2xl font-bold tracking-tight">Conversation</h2>
        <p className="text-muted-foreground">
          Chat history with {conversation.customer?.name || conversation.whatsapp_number}
        </p>
      </div>

      <ChatInterface 
        conversationId={id}
        initialMessages={messages || []}
        customerName={conversation.customer?.name || 'Unknown Customer'}
        customerPhone={conversation.whatsapp_number}
      />
    </div>
  )
}
