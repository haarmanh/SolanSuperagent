import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  BarChart3,
  Brain,
  Sparkles,
  Database,
  Settings,
  Home,
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Coherence Analytics', href: '/coherence', icon: Brain },
  { name: 'Cognitive Insights', href: '/cognitive', icon: Sparkles },
  { name: 'Memory History', href: '/memory', icon: Database },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <div className="w-64 bg-card border-r border-border">
      <div className="p-6">
        <div className="flex items-center space-x-2">
          <Brain className="h-8 w-8 text-solan-600" />
          <div>
            <h1 className="text-xl font-bold text-foreground">Solan</h1>
            <p className="text-sm text-muted-foreground">Superagent</p>
          </div>
        </div>
      </div>
      
      <nav className="px-4 space-y-2">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                'flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          )
        })}
      </nav>
      
      <div className="absolute bottom-4 left-4 right-4">
        <div className="bg-muted rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm font-medium">System Status</span>
          </div>
          <p className="text-xs text-muted-foreground">
            Coherence monitoring active
          </p>
        </div>
      </div>
    </div>
  )
}
