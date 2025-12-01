import { createClient } from '@/lib/supabase/server'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

export default async function CustomersPage() {
  const supabase = await createClient()
  
  const { data: customers } = await supabase
    .from('customers')
    .select('*')
    .order('created_at', { ascending: false })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Customers</h2>
          <p className="text-muted-foreground">
            View your customer base.
          </p>
        </div>
      </div>

      <div className="rounded-md border bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>WhatsApp</TableHead>
              <TableHead>Total Spent</TableHead>
              <TableHead>Orders</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {customers?.map((customer) => (
              <TableRow key={customer.id}>
                <TableCell className="font-medium">{customer.name || 'Unknown'}</TableCell>
                <TableCell>{customer.whatsapp_number}</TableCell>
                <TableCell>${customer.total_spent}</TableCell>
                <TableCell>{customer.total_orders}</TableCell>
              </TableRow>
            ))}
            {(!customers || customers.length === 0) && (
              <TableRow>
                <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                  No customers found yet.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
