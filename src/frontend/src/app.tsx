import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import Layout from '@/components/layout/Layout'
import Dashboard from '@/pages/Dashboard'
import CoherenceAnalytics from '@/pages/CoherenceAnalytics'
import CognitiveInsights from '@/pages/CognitiveInsights'
import MemoryHistory from '@/pages/MemoryHistory'
import Settings from '@/pages/Settings'

function App() {
  return (
    <div className="min-h-screen bg-background">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/coherence" element={<CoherenceAnalytics />} />
          <Route path="/cognitive" element={<CognitiveInsights />} />
          <Route path="/memory" element={<MemoryHistory />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
      <Toaster />
    </div>
  )
}

export default App
