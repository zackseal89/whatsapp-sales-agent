'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Bell, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

export function OrderNotification() {
  const [notification, setNotification] = useState<{
    id: string
    message: string
    amount: number
  } | null>(null)
  
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel('orders-channel')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'orders',
        },
        (payload) => {
          console.log('New order received!', payload)
          const newOrder = payload.new as any
          setNotification({
            id: newOrder.id,
            message: `New order #${newOrder.order_number} received!`,
            amount: newOrder.total
          })
          
          // Play a sound if possible
          try {
            const audio = new Audio('/notification.mp3') // Assumes file exists or fails silently
            audio.play().catch(e => console.log('Audio play failed', e))
          } catch (e) {
            // Ignore audio errors
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  if (!notification) return null

  return (
    <div className="fixed bottom-4 right-4 z-50 animate-in slide-in-from-bottom-5 fade-in duration-300">
      <Card className="p-4 shadow-lg border-l-4 border-l-green-500 flex items-start gap-4 w-80 bg-white dark:bg-slate-950">
        <div className="bg-green-100 dark:bg-green-900/30 p-2 rounded-full">
          <Bell className="h-5 w-5 text-green-600 dark:text-green-400" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-sm">New Order Received!</h4>
          <p className="text-sm text-muted-foreground mt-1">
            {notification.message}
          </p>
          <p className="text-sm font-medium mt-1">
            Amount: ${notification.amount}
          </p>
          <div className="mt-3 flex gap-2">
            <Button 
              size="sm" 
              variant="default" 
              className="w-full text-xs"
              onClick={() => window.location.reload()} // Refresh to see order
            >
              View Orders
            </Button>
            <Button 
              size="sm" 
              variant="ghost" 
              className="w-auto px-2"
              onClick={() => setNotification(null)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
