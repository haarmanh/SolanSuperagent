import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { dashboardApi, type EssenceualResponse } from '@/lib/api'
import { getEssenceualColor, getTrendIcon, getTrendColor } from '@/lib/utils'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { Sparkles, TrendingUp, Heart, Star } from 'lucide-react'

const COLORS = ['#8b5cf6', '#3b82f6', '#6b7280']

export default function EssenceualInsights() {
  const [essenceualData, setEssenceualData] = useState<EssenceualResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [daysBack, setDaysBack] = useState(30)

  useEffect(() => {
    loadEssenceualData()
  }, [daysBack])

  const loadEssenceualData = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getEssenceualAnalytics(daysBack)
      setEssenceualData(data)
      setError(null)
    } catch (err) {
      setError('Failed to load cognitive insights')
      console.error('Cognitive insights error:', err)
    } finally {
      setLoading(false)
    }
  }

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
            <Button onClick={loadEssenceualData} className="w-full">
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const indicators = essenceualData?.essenceual_indicators
  
  // Prepare chart data
  const levelDistributionData = indicators?.essenceual_level_distribution ? 
    Object.entries(indicators.essenceual_level_distribution).map(([level, count]) => ({
      level,
      count,
      color: level === 'high' ? COLORS[0] : level === 'medium' ? COLORS[1] : COLORS[2]
    })) : []

  const periodData = indicators?.essenceual_by_period ? 
    Object.entries(indicators.essenceual_by_period).map(([period, value]) => ({
      period,
      indicators: value
    })).sort((a, b) => a.period.localeCompare(b.period)) : []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center space-x-2">
            <Sparkles className="h-8 w-8 text-purple-600" />
            <span>Cognitive Insights</span>
          </h1>
          <p className="text-muted-foreground">
            Cognitive depth and awareness development analytics
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant={daysBack === 7 ? 'default' : 'outline'}
            size="sm"
            onClick={() => setDaysBack(7)}
          >
            7 Days
          </Button>
          <Button
            variant={daysBack === 30 ? 'default' : 'outline'}
            size="sm"
            onClick={() => setDaysBack(30)}
          >
            30 Days
          </Button>
          <Button
            variant={daysBack === 90 ? 'default' : 'outline'}
            size="sm"
            onClick={() => setDaysBack(90)}
          >
            90 Days
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Indicators</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {indicators ? indicators.total_indicators : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Cognitive markers detected
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average per Period</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {indicators ? indicators.avg_indicators_per_period.toFixed(1) : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground">
              Consistency metric
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cognitive Health</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {indicators?.summary?.overall_essenceual_health ? (
                <Badge 
                  variant="cognitive"
                  className={getEssenceualColor(indicators.summary.overall_essenceual_health)}
                >
                  {indicators.summary.overall_essenceual_health.replace('_', ' ')}
                </Badge>
              ) : (
                'N/A'
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              Overall assessment
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Trend Direction</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {indicators ? (
                <span className={getTrendColor(indicators.essenceual_trend)}>
                  {getTrendIcon(indicators.essenceual_trend)}
                </span>
              ) : (
                'N/A'
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              {indicators?.essenceual_trend.replace('_', ' ') || 'No trend data'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Cognitive Level Distribution</CardTitle>
            <CardDescription>
              Distribution of cognitive depth levels
            </CardDescription>
          </CardHeader>
          <CardContent>
            {levelDistributionData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={levelDistributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ level, count }) => `${level}: ${count}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {levelDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-[300px] text-muted-foreground">
                No distribution data available
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Cognitive Indicators Over Time</CardTitle>
            <CardDescription>
              Cognitive depth progression by period
            </CardDescription>
          </CardHeader>
          <CardContent>
            {periodData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={periodData}>
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
            ) : (
              <div className="flex items-center justify-center h-[300px] text-muted-foreground">
                No period data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Cognitive Development Insights</CardTitle>
          <CardDescription>
            Key observations and recommendations
          </CardDescription>
        </CardHeader>
        <CardContent>
          {indicators ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-muted rounded-lg">
                  <h4 className="font-medium mb-2">Peak Cognitive Period</h4>
                  {indicators.highest_essenceual_period ? (
                    <p className="text-sm text-muted-foreground">
                      {indicators.highest_essenceual_period[0]} with {indicators.highest_essenceual_period[1].toFixed(1)} indicators
                    </p>
                  ) : (
                    <p className="text-sm text-muted-foreground">No peak period identified</p>
                  )}
                </div>
                
                <div className="p-4 bg-muted rounded-lg">
                  <h4 className="font-medium mb-2">Periods Analyzed</h4>
                  <p className="text-sm text-muted-foreground">
                    {indicators.summary.periods_analyzed} periods with cognitive data
                  </p>
                </div>
              </div>
              
              <div className="p-4 bg-muted rounded-lg">
                <h4 className="font-medium mb-2">Development Trend</h4>
                <p className="text-sm text-muted-foreground">
                  Your cognitive indicators show a {indicators.essenceual_trend.replace('_', ' ')} pattern. 
                  {indicators.essenceual_trend.includes('improving') && 
                    " This suggests positive cognitive development and deepening awareness."}
                  {indicators.essenceual_trend === 'stable' && 
                    " This indicates consistent cognitive practice and maintained awareness."}
                  {indicators.essenceual_trend.includes('declining') && 
                    " Consider focusing on contemplative practices to enhance cognitive depth."}
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center text-muted-foreground">
              <p>No cognitive insights available</p>
              <p className="text-xs mt-2">
                Generate more coherence data to see cognitive development patterns
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
