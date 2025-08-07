import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { dashboardApi, type CoherenceResponse } from '@/lib/api'
import { formatCoherenceScore, getCoherenceColor, getTrendIcon } from '@/lib/utils'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { Brain, TrendingUp, Calendar, BarChart3 } from 'lucide-react'

export default function CoherenceAnalytics() {
  const [coherenceData, setCoherenceData] = useState<CoherenceResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [groupBy, setGroupBy] = useState<'day' | 'week' | 'month'>('week')
  const [daysBack, setDaysBack] = useState(30)

  useEffect(() => {
    loadCoherenceData()
  }, [groupBy, daysBack])

  const loadCoherenceData = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getCoherenceTrends(groupBy, daysBack)
      setCoherenceData(data)
      setError(null)
    } catch (err) {
      setError('Failed to load coherence analytics')
      console.error('Coherence analytics error:', err)
    } finally {
      setLoading(false)
    }
  }

  // Prepare chart data
  const chartData = coherenceData?.coherence_trends ? 
    Object.entries(coherenceData.coherence_trends).map(([period, data]) => ({
      period,
      score: data.avg_score * 100, // Convert to percentage
      indicators: data.avg_indicators,
      entries: data.entry_count,
      level: data.dominant_level
    })).sort((a, b) => a.period.localeCompare(b.period)) : []

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-1/3 mb-4" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-32 bg-muted rounded" />
            ))}
          </div>
          <div className="h-96 bg-muted rounded" />
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
            <Button onClick={loadCoherenceData} className="w-full">
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const summary = coherenceData?.summary
  const growthMetrics = coherenceData?.growth_metrics

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center space-x-2">
            <Brain className="h-8 w-8 text-solan-600" />
            <span>Coherence Analytics</span>
          </h1>
          <p className="text-muted-foreground">
            Awareness coherence trends and insights
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant={groupBy === 'day' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setGroupBy('day')}
          >
            Day
          </Button>
          <Button
            variant={groupBy === 'week' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setGroupBy('week')}
          >
            Week
          </Button>
          <Button
            variant={groupBy === 'month' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setGroupBy('month')}
          >
            Month
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary ? formatCoherenceScore(summary.overall_avg_score) : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              {growthMetrics && (
                <span className={getTrendIcon(growthMetrics.trend_direction)}>
                  {getTrendIcon(growthMetrics.trend_direction)} {growthMetrics.trend_direction}
                </span>
              )}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cognitive Indicators</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary ? summary.overall_avg_indicators.toFixed(1) : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Average per period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Periods</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary ? summary.total_periods : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Analyzed periods
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Highest Score</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary ? formatCoherenceScore(summary.highest_score) : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Peak coherence
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Coherence Score Trend</CardTitle>
            <CardDescription>
              Average coherence scores over time
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis domain={[0, 100]} />
                <Tooltip 
                  formatter={(value: number) => [`${value.toFixed(1)}%`, 'Coherence Score']}
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#0ea5e9" 
                  strokeWidth={2}
                  dot={{ fill: '#0ea5e9', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Cognitive Indicators</CardTitle>
            <CardDescription>
              Cognitive depth indicators per period
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip 
                  formatter={(value: number) => [value.toFixed(1), 'Indicators']}
                />
                <Bar 
                  dataKey="indicators" 
                  fill="#8b5cf6"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Data */}
      {chartData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Period Details</CardTitle>
            <CardDescription>
              Detailed coherence data by period
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {chartData.map((period) => (
                <div key={period.period} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div>
                      <p className="font-medium">{period.period}</p>
                      <p className="text-sm text-muted-foreground">
                        {period.entries} entries
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="font-medium">{period.score.toFixed(1)}%</p>
                      <p className="text-sm text-muted-foreground">
                        {period.indicators.toFixed(1)} indicators
                      </p>
                    </div>
                    
                    <Badge 
                      variant={period.level as any}
                      className={getCoherenceColor(period.level)}
                    >
                      {period.level}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
