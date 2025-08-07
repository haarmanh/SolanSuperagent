import axios from 'axios'

// API base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Types
export interface CoherenceTrend {
  period: string
  avg_score: number
  avg_indicators: number
  dominant_level: string
  entry_count: number
  score_range: {
    min: number
    max: number
  }
  level_distribution: Record<string, number>
}

export interface CoherenceResponse {
  success: boolean
  coherence_trends: Record<string, CoherenceTrend>
  summary: {
    overall_avg_score: number
    overall_avg_indicators: number
    score_trend: string
    source_distribution: Record<string, number>
    total_periods: number
    highest_score: number
    lowest_score: number
    most_essenceual_day: string
  }
  growth_metrics: {
    score_growth: number
    indicator_growth: number
    growth_percentage: number
    trend_direction: string
  }
  metadata: {
    total_entries: number
    date_range: {
      start: string
      end: string
    }
    group_by: string
    generated_at: string
  }
  dashboard_ready: boolean
  last_updated: string
}

export interface CognitiveResponse {
  success: boolean
  essenceual_indicators: {
    total_indicators: number
    avg_indicators_per_period: number
    essenceual_by_period: Record<string, number>
    essenceual_level_distribution: Record<string, number>
    highest_essenceual_period: [string, number] | null
    essenceual_trend: string
    summary: {
      periods_analyzed: number
      overall_essenceual_health: string
    }
  }
  dashboard_ready: boolean
  last_updated: string
}

export interface MemoryEntry {
  agent: string
  memory_id: string
  timestamp: string
  coherence_tags: string[]
  content_preview: string
  emotional_weight: number
  moral_significance: number
}

export interface MemoryResponse {
  success: boolean
  memory_coherence: {
    entries: MemoryEntry[]
    agents: string[]
    total_entries: number
    date_range: {
      start: string
      end: string
    }
  }
  dashboard_ready: boolean
  last_updated: string
}

export interface OverviewResponse {
  success: boolean
  overview: {
    coherence: {
      available: boolean
      summary: any
      growth_metrics: any
    }
    cognitive: {
      available: boolean
      indicators: any
    }
    memory: {
      available: boolean
      recent_entries: number
    }
  }
  dashboard_ready: boolean
  last_updated: string
}

// API functions
export const dashboardApi = {
  // Get coherence trends
  getCoherenceTrends: async (
    groupBy: 'day' | 'week' | 'month' = 'week',
    daysBack: number = 30
  ): Promise<CoherenceResponse> => {
    const response = await api.get('/dashboard/coherence', {
      params: { group_by: groupBy, days_back: daysBack }
    })
    return response.data
  },

  // Get cognitive analytics
  getCognitiveAnalytics: async (daysBack: number = 30): Promise<CognitiveResponse> => {
    const response = await api.get('/dashboard/cognitive', {
      params: { days_back: daysBack }
    })
    return response.data
  },

  // Get memory coherence history
  getMemoryHistory: async (
    agent?: string,
    limit: number = 50
  ): Promise<MemoryResponse> => {
    const response = await api.get('/dashboard/history', {
      params: { agent, limit }
    })
    return response.data
  },

  // Get dashboard overview
  getOverview: async (): Promise<OverviewResponse> => {
    const response = await api.get('/dashboard/overview')
    return response.data
  },
}

export default api
