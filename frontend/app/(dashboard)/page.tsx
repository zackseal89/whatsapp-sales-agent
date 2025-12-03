import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageSquare, ShoppingCart, Users, DollarSign } from "lucide-react"
import { createClient } from "@/lib/supabase/server"

export const dynamic = 'force-dynamic'

interface DashboardStats {
  totalRevenue: number
  revenueGrowth: number
  activeConversations: number
  conversationsGrowth: number
  totalOrders: number
  ordersGrowth: number
  activeCustomers: number
  customersGrowth: number
}

async function getDashboardStats(): Promise<DashboardStats> {
  const supabase = await createClient()
  
  // Get current month and last month date ranges
  const now = new Date()
  const currentMonthStart = new Date(now.getFullYear(), now.getMonth(), 1)
  const lastMonthStart = new Date(now.getFullYear(), now.getMonth() - 1, 1)
  const lastMonthEnd = new Date(now.getFullYear(), now.getMonth(), 0, 23, 59, 59)
  
  try {
    // Total Revenue - sum of confirmed/delivered orders
    const { data: revenueData } = await supabase
      .from('orders')
      .select('total')
      .in('status', ['confirmed', 'delivered', 'shipped'])
    
    const totalRevenue = revenueData?.reduce((sum, order) => sum + Number(order.total || 0), 0) || 0
    
    // Last month revenue
    const { data: lastMonthRevenueData } = await supabase
      .from('orders')
      .select('total')
      .in('status', ['confirmed', 'delivered', 'shipped'])
      .gte('created_at', lastMonthStart.toISOString())
      .lte('created_at', lastMonthEnd.toISOString())
    
    const lastMonthRevenue = lastMonthRevenueData?.reduce((sum, order) => sum + Number(order.total || 0), 0) || 0
    const revenueGrowth = lastMonthRevenue > 0 ? ((totalRevenue - lastMonthRevenue) / lastMonthRevenue) * 100 : 0
    
    // Active Conversations
    const { count: activeConversations } = await supabase
      .from('conversations')
      .select('*', { count: 'exact', head: true })
      .eq('status', 'active')
    
    const { count: lastMonthConversations } = await supabase
      .from('conversations')
      .select('*', { count: 'exact', head: true })
      .eq('status', 'active')
      .gte('created_at', lastMonthStart.toISOString())
      .lte('created_at', lastMonthEnd.toISOString())
    
    const conversationsGrowth = (lastMonthConversations || 0) > 0 
      ? (((activeConversations || 0) - (lastMonthConversations || 0)) / (lastMonthConversations || 0)) * 100 
      : 0
    
    // Total Orders
    const { count: totalOrders } = await supabase
      .from('orders')
      .select('*', { count: 'exact', head: true })
    
    const { count: lastMonthOrders } = await supabase
      .from('orders')
      .select('*', { count: 'exact', head: true })
      .gte('created_at', lastMonthStart.toISOString())
      .lte('created_at', lastMonthEnd.toISOString())
    
    const ordersGrowth = (lastMonthOrders || 0) > 0 
      ? (((totalOrders || 0) - (lastMonthOrders || 0)) / (lastMonthOrders || 0)) * 100 
      : 0
    
    // Active Customers
    const { count: activeCustomers } = await supabase
      .from('customers')
      .select('*', { count: 'exact', head: true })
    
    const { count: lastMonthCustomers } = await supabase
      .from('customers')
      .select('*', { count: 'exact', head: true })
      .gte('created_at', lastMonthStart.toISOString())
      .lte('created_at', lastMonthEnd.toISOString())
    
    const customersGrowth = (lastMonthCustomers || 0) > 0 
      ? (((activeCustomers || 0) - (lastMonthCustomers || 0)) / (lastMonthCustomers || 0)) * 100 
      : 0
    
    return {
      totalRevenue,
      revenueGrowth,
      activeConversations: activeConversations || 0,
      conversationsGrowth,
      totalOrders: totalOrders || 0,
      ordersGrowth,
      activeCustomers: activeCustomers || 0,
      customersGrowth,
    }
  } catch (error) {
    console.error('Error fetching dashboard stats:', error)
    // Return zeros if there's an error
    return {
      totalRevenue: 0,
      revenueGrowth: 0,
      activeConversations: 0,
      conversationsGrowth: 0,
      totalOrders: 0,
      ordersGrowth: 0,
      activeCustomers: 0,
      customersGrowth: 0,
    }
  }
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount)
}

function formatGrowth(growth: number): string {
  const sign = growth > 0 ? '+' : ''
  return `${sign}${growth.toFixed(1)}%`
}

export default async function DashboardPage() {
  const stats = await getDashboardStats()
  
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">Overview of your sales agent performance.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(stats.totalRevenue)}</div>
            <p className="text-xs text-muted-foreground">
              {formatGrowth(stats.revenueGrowth)} from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Conversations</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeConversations}</div>
            <p className="text-xs text-muted-foreground">
              {formatGrowth(stats.conversationsGrowth)} from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Orders</CardTitle>
            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalOrders}</div>
            <p className="text-xs text-muted-foreground">
              {formatGrowth(stats.ordersGrowth)} from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeCustomers}</div>
            <p className="text-xs text-muted-foreground">
              {formatGrowth(stats.customersGrowth)} from last month
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
