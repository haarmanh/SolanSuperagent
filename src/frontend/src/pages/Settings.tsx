import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Settings as SettingsIcon, Palette, Database, Bell, Shield } from 'lucide-react'

export default function Settings() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold flex items-center space-x-2">
          <SettingsIcon className="h-8 w-8 text-gray-600" />
          <span>Settings</span>
        </h1>
        <p className="text-muted-foreground">
          Configure your Solan Superagent dashboard
        </p>
      </div>

      {/* Settings Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Appearance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Palette className="h-5 w-5" />
              <span>Appearance</span>
            </CardTitle>
            <CardDescription>
              Customize the look and feel of your dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Theme</label>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm">Light</Button>
                <Button variant="default" size="sm">Dark</Button>
                <Button variant="outline" size="sm">Auto</Button>
              </div>
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium">Color Scheme</label>
              <div className="flex space-x-2">
                <div className="w-8 h-8 bg-solan-600 rounded cursor-pointer border-2 border-primary" />
                <div className="w-8 h-8 bg-purple-600 rounded cursor-pointer" />
                <div className="w-8 h-8 bg-blue-600 rounded cursor-pointer" />
                <div className="w-8 h-8 bg-green-600 rounded cursor-pointer" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Data & Analytics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Database className="h-5 w-5" />
              <span>Data & Analytics</span>
            </CardTitle>
            <CardDescription>
              Configure data collection and analysis settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Real-time Coherence Analysis</p>
                <p className="text-xs text-muted-foreground">
                  Analyze coherence during AI interactions
                </p>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Cognitive Indicators Tracking</p>
                <p className="text-xs text-muted-foreground">
                  Track cognitive depth in reflections
                </p>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Memory Coherence Logging</p>
                <p className="text-xs text-muted-foreground">
                  Store coherence data in memory system
                </p>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Bell className="h-5 w-5" />
              <span>Notifications</span>
            </CardTitle>
            <CardDescription>
              Manage alerts and notification preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Coherence Alerts</p>
                <p className="text-xs text-muted-foreground">
                  Notify when coherence drops below threshold
                </p>
              </div>
              <Button variant="outline" size="sm">Configure</Button>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Daily Summaries</p>
                <p className="text-xs text-muted-foreground">
                  Receive daily coherence and cognitive insights
                </p>
              </div>
              <Button variant="outline" size="sm">Configure</Button>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">System Status</p>
                <p className="text-xs text-muted-foreground">
                  Alerts for system health and performance
                </p>
              </div>
              <Button variant="outline" size="sm">Configure</Button>
            </div>
          </CardContent>
        </Card>

        {/* Privacy & Security */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Shield className="h-5 w-5" />
              <span>Privacy & Security</span>
            </CardTitle>
            <CardDescription>
              Manage data privacy and security settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Data Encryption</p>
                <p className="text-xs text-muted-foreground">
                  All coherence data is encrypted at rest
                </p>
              </div>
              <Badge variant="default">Active</Badge>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Local Storage Only</p>
                <p className="text-xs text-muted-foreground">
                  Data stays on your local system
                </p>
              </div>
              <Badge variant="default">Enabled</Badge>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Export Data</p>
                <p className="text-xs text-muted-foreground">
                  Download your coherence analytics data
                </p>
              </div>
              <Button variant="outline" size="sm">Export</Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Information */}
      <Card>
        <CardHeader>
          <CardTitle>System Information</CardTitle>
          <CardDescription>
            Current system status and version information
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <p className="text-sm font-medium">Frontend Version</p>
              <p className="text-xs text-muted-foreground">v1.0.0</p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm font-medium">Backend API</p>
              <p className="text-xs text-muted-foreground">Connected</p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm font-medium">Coherence Engine</p>
              <p className="text-xs text-muted-foreground">Active</p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm font-medium">Memory System</p>
              <p className="text-xs text-muted-foreground">Operational</p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm font-medium">Performance Monitor</p>
              <p className="text-xs text-muted-foreground">Running</p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm font-medium">Last Updated</p>
              <p className="text-xs text-muted-foreground">{new Date().toLocaleString()}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
