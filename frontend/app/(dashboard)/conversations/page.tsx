import { createClient } from '@/lib/supabase/server'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { formatDistanceToNow } from 'date-fns'
import { MessageSquare, MoreHorizontal } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default async function ConversationsPage() {
  const supabase = await createClient()
  
  const { data: conversations } = await supabase
    .from('conversations')
    .select(`
      *,
      customer:customers(name, whatsapp_number)
    `)
    .order('last_message_at', { ascending: false })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Conversations</h2>
          <p className="text-muted-foreground">
            Monitor and manage customer interactions.
          </p>
        </div>
      </div>

      <div className="rounded-md border bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Customer</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Messages</TableHead>
              <TableHead>Last Active</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {conversations?.map((conversation) => (
              <TableRow key={conversation.id}>
                <TableCell>
                  <div className="font-medium">
                    {conversation.customer?.name || 'Unknown'}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {conversation.whatsapp_number}
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant={conversation.status === 'active' ? 'default' : 'secondary'}>
                    {conversation.status}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4 text-muted-foreground" />
                    <span>{conversation.message_count}</span>
                  </div>
                </TableCell>
                <TableCell>
                  {conversation.last_message_at && formatDistanceToNow(new Date(conversation.last_message_at), { addSuffix: true })}
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <span className="sr-only">Open menu</span>
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem>View details</DropdownMenuItem>
                      <DropdownMenuItem>Archive conversation</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
            {(!conversations || conversations.length === 0) && (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                  No conversations found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
