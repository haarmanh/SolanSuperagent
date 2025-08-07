import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { dashboardApi, type MemoryResponse, type MemoryEntry } from '@/lib/api'
import { formatDateTime, getCoherenceColor } from '@/lib/utils'
import { Database, User, Clock, Tag } from 'lucide-react'

export default function MemoryHistory() {
  const [memoryData, setMemoryData] = useState<MemoryResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<string>('all')
  const [limit, setLimit] = useState(50)

  useEffect(() => {
    loadMemoryData()
  }, [selectedAgent, limit])

  const loadMemoryData = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getMemoryHistory(
        selectedAgent === 'all' ? undefined : selectedAgent,
        limit
      )
      setMemoryData(data)
      setError(null)
    } catch (err) {
      setError('Failed to load memory history')
      console.error('Memory history error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-1/3 mb-4" />
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-24 bg-muted rounded" />
            ))}
          </div>
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
            <Button onClick={loadMemoryData} className="w-full">
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const memoryEntries = memoryData?.memory_coherence?.entries || []
  const availableAgents = memoryData?.memory_coherence?.agents || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center space-x-2">
            <Database className="h-8 w-8 text-blue-600" />
            <span>Memory History</span>
          </h1>
          <p className="text-muted-foreground">
            Coherence-tagged memories from AI agents
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant={selectedAgent === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedAgent('all')}
          >
            All Agents
          </Button>
          {availableAgents.map((agent) => (
            <Button
              key={agent}
              variant={selectedAgent === agent ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedAgent(agent)}
            >
              {agent.charAt(0).toUpperCase() + agent.slice(1)}
            </Button>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Entries</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {memoryData?.memory_coherence?.total_entries || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Coherence-tagged memories
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {availableAgents.length}
            </div>
            <p className="text-xs text-muted-foreground">
              {availableAgents.join(', ') || 'None'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Date Range</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-sm font-bold">
              {memoryData?.memory_coherence?.date_range ? (
                <>
                  <div>{new Date(memoryData.memory_coherence.date_range.start).toLocaleDateString()}</div>
                  <div className="text-xs text-muted-foreground">
                    to {new Date(memoryData.memory_coherence.date_range.end).toLocaleDateString()}
                  </div>
                </>
              ) : (
                'No date range'
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Showing</CardTitle>
            <Tag className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {memoryEntries.length}
            </div>
            <p className="text-xs text-muted-foreground">
              of {memoryData?.memory_coherence?.total_entries || 0} entries
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Memory Entries */}
      <Card>
        <CardHeader>
          <CardTitle>Memory Entries</CardTitle>
          <CardDescription>
            Recent memories with coherence analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          {memoryEntries.length > 0 ? (
            <div className="space-y-4">
              {memoryEntries.map((entry: MemoryEntry, index) => (
                <div key={entry.memory_id || index} className="border rounded-lg p-4 space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">
                        {entry.agent}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {formatDateTime(entry.timestamp)}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {entry.coherence_tags.map((tag, tagIndex) => {
                        const level = tag.replace('coherentie_', '')
                        return (
                          <Badge 
                            key={tagIndex}
                            variant={level as any}
                            className={getCoherenceColor(level)}
                          >
                            {level}
                          </Badge>
                        )
                      })}
                    </div>
                  </div>
                  
                  <div className="text-sm">
                    <p className="text-foreground">{entry.content_preview}</p>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <div className="flex items-center space-x-4">
                      <span>Emotional Weight: {entry.emotional_weight.toFixed(1)}</span>
                      <span>Moral Significance: {entry.moral_significance.toFixed(1)}</span>
                    </div>
                    <span>ID: {entry.memory_id}</span>
                  </div>
                </div>
              ))}
              
              {memoryEntries.length >= limit && (
                <div className="text-center pt-4">
                  <Button 
                    variant="outline" 
                    onClick={() => setLimit(limit + 25)}
                  >
                    Load More Entries
                  </Button>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <Database className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No memory entries found</p>
              <p className="text-xs mt-2">
                {selectedAgent === 'all' 
                  ? 'No coherence-tagged memories available from any agent'
                  : `No coherence-tagged memories available from ${selectedAgent}`
                }
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
