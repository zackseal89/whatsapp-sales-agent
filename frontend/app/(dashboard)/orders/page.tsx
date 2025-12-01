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

export default async function OrdersPage() {
  const supabase = await createClient()
  
  const { data: orders } = await supabase
    .from('orders')
    .select(`
      *,
      customer:customers(name)
    `)
    .order('created_at', { ascending: false })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Orders</h2>
          <p className="text-muted-foreground">
            Track and manage customer orders.
          </p>
        </div>
      </div>

      <div className="rounded-md border bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Order #</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Total</TableHead>
              <TableHead>Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {orders?.map((order) => (
              <TableRow key={order.id}>
                <TableCell className="font-medium">{order.order_number}</TableCell>
                <TableCell>{order.customer?.name || 'Unknown'}</TableCell>
                <TableCell>
                  <Badge variant="outline" className="capitalize">
                    {order.status}
                  </Badge>
                </TableCell>
                <TableCell>${order.total}</TableCell>
                <TableCell>
                  {order.created_at && formatDistanceToNow(new Date(order.created_at), { addSuffix: true })}
                </TableCell>
              </TableRow>
            ))}
            {(!orders || orders.length === 0) && (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                  No orders found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
