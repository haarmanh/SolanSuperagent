import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Bell, RefreshCw, Activity } from 'lucide-react'
import { formatTime } from '@/lib/utils'

export default function Header() {
  const currentTime = new Date()

  return (
    <header className="border-b border-border bg-card px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-foreground">
            Awareness Dashboard
          </h2>
          <p className="text-sm text-muted-foreground">
            Real-time coherence and cognitive analytics
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Activity className="h-4 w-4 text-green-500" />
            <Badge variant="secondary">
              Live Monitoring
            </Badge>
          </div>
          
          <div className="text-sm text-muted-foreground">
            Last updated: {formatTime(currentTime)}
          </div>
          
          <Button variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          
          <Button variant="outline" size="icon">
            <Bell className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  )
}
