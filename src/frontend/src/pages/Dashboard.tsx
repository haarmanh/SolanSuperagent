import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { dashboardApi, type OverviewResponse } from '@/lib/api'
import { formatCoherenceScore, getTrendIcon, getTrendColor } from '@/lib/utils'
import { Brain, Sparkles, Database, TrendingUp, Activity } from 'lucide-react'

export default function Dashboard() {
  const [overview, setOverview] = useState<OverviewResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadOverview()
  }, [])

  const loadOverview = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getOverview()
      setOverview(data)
      setError(null)
    } catch (err) {
      setError('Failed to load dashboard overview')
      console.error('Dashboard overview error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-4 bg-muted rounded w-3/4" />
                <div className="h-3 bg-muted rounded w-1/2" />
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-muted rounded w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
          <CardContent>
            <button
              onClick={loadOverview}
              className="w-full bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"
            >
              Retry
            </button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const coherenceData = overview?.overview?.coherence
  const essenceualData = overview?.overview?.cognitive
  const memoryData = overview?.overview?.memory

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Coherence Status</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {coherenceData?.available ? (
                formatCoherenceScore(coherenceData.summary?.overall_avg_score || 0)
              ) : (
                'N/A'
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              {coherenceData?.available ? (
                <span className={getTrendColor(coherenceData.growth_metrics?.trend_direction || '')}>
                  {getTrendIcon(coherenceData.growth_metrics?.trend_direction || '')} 
                  {coherenceData.growth_metrics?.trend_direction || 'stable'}
                </span>
              ) : (
                'No data available'
              )}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cognitive Indicators</CardTitle>
            <Sparkles className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {essenceualData?.available ? (
                essenceualData.indicators?.total_indicators || 0
              ) : (
                'N/A'
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              {essenceualData?.available ? (
                `Health: ${essenceualData.indicators?.summary?.overall_essenceual_health || 'unknown'}`
              ) : (
                'No data available'
              )}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Memory Entries</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {memoryData?.available ? (
                memoryData.recent_entries || 0
              ) : (
                'N/A'
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              Recent coherence entries
            </p>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>System Health</span>
            </CardTitle>
            <CardDescription>
              Real-time monitoring status
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Coherence Analytics</span>
                <Badge variant={coherenceData?.available ? "default" : "secondary"}>
                  {coherenceData?.available ? "Active" : "Inactive"}
                </Badge>
              </div>
              <Progress value={coherenceData?.available ? 100 : 0} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Cognitive Monitoring</span>
                <Badge variant={essenceualData?.available ? "default" : "secondary"}>
                  {essenceualData?.available ? "Active" : "Inactive"}
                </Badge>
              </div>
              <Progress value={essenceualData?.available ? 100 : 0} />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Memory Integration</span>
                <Badge variant={memoryData?.available ? "default" : "secondary"}>
                  {memoryData?.available ? "Active" : "Inactive"}
                </Badge>
              </div>
              <Progress value={memoryData?.available ? 100 : 0} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5" />
              <span>Quick Insights</span>
            </CardTitle>
            <CardDescription>
              Latest analytics summary
            </CardDescription>
          </CardHeader>
          <CardContent>
            {overview?.success ? (
              <div className="space-y-4">
                <div className="text-sm">
                  <p className="font-medium mb-2">Recent Activity:</p>
                  <ul className="space-y-1 text-muted-foreground">
                    {coherenceData?.available && (
                      <li>• Coherence monitoring active</li>
                    )}
                    {essenceualData?.available && (
                      <li>• Cognitive indicators tracked</li>
                    )}
                    {memoryData?.available && (
                      <li>• Memory coherence logged</li>
                    )}
                    <li>• Dashboard updated: {new Date().toLocaleTimeString()}</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-center text-muted-foreground">
                <p>No recent activity data available</p>
                <p className="text-xs mt-2">
                  Start generating coherence data to see insights
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
