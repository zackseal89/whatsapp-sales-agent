import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">
          Manage your account and agent configuration.
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile Information</CardTitle>
            <CardDescription>Update your account details.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" defaultValue="admin@example.com" disabled />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="name">Display Name</Label>
              <Input id="name" defaultValue="Admin User" />
            </div>
            <Button>Save Changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>AI Agent Configuration</CardTitle>
            <CardDescription>Customize how your agent behaves.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="greeting">Greeting Message</Label>
              <Input id="greeting" defaultValue="Hello! How can I help you today?" />
            </div>
            <Button variant="outline">Update Agent</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
