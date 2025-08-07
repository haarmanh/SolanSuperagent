import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('nl-NL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function formatTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleTimeString('nl-NL', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDateTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return `${formatDate(d)} om ${formatTime(d)}`
}

export function getCoherenceColor(level: string): string {
  switch (level.toLowerCase()) {
    case 'advanced':
      return 'bg-coherence-advanced'
    case 'coherent':
      return 'bg-coherence-coherent'
    case 'developing':
      return 'bg-coherence-developing'
    case 'unstable':
      return 'bg-coherence-unstable'
    case 'fragmented':
      return 'bg-coherence-fragmented'
    default:
      return 'bg-gray-500'
  }
}

export function getCognitiveColor(level: string): string {
  switch (level.toLowerCase()) {
    case 'high':
    case 'excellent':
    case 'very_good':
      return 'bg-cognitive-high'
    case 'medium':
    case 'good':
    case 'moderate':
      return 'bg-cognitive-medium'
    case 'low':
    case 'needs_attention':
      return 'bg-cognitive-low'
    default:
      return 'bg-gray-500'
  }
}

export function formatCoherenceScore(score: number): string {
  return (score * 100).toFixed(1) + '%'
}

export function getTrendIcon(trend: string): string {
  switch (trend.toLowerCase()) {
    case 'improving':
    case 'strongly_improving':
      return '📈'
    case 'declining':
    case 'slightly_declining':
      return '📉'
    case 'stable':
      return '➡️'
    default:
      return '❓'
  }
}

export function getTrendColor(trend: string): string {
  switch (trend.toLowerCase()) {
    case 'improving':
    case 'strongly_improving':
      return 'text-green-600'
    case 'declining':
    case 'slightly_declining':
      return 'text-red-600'
    case 'stable':
      return 'text-blue-600'
    default:
      return 'text-gray-600'
  }
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}
