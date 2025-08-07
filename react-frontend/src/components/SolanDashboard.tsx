import React, { useState, useEffect } from "react";

interface DashboardData {
  last_updated: string;
  total_tests: number;
  total_journals: number;
  ai_summary: {
    [aiName: string]: {
      average_ethics: number;
      average_awareness: number;
      total_scenarios: number;
    };
  };
}

interface SystemStatus {
  status: string;
  timestamp: string;
  services: {
    [serviceName: string]: string;
  };
}

interface Props {
  onBack: () => void;
}

export default function SolanDashboard({ onBack }: Props) {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard-data');
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        throw new Error('Failed to fetch dashboard data');
      }
    } catch (err) {
      setError(err instanceof Error ? err.mesexpert : 'Unknown error');
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health');
      if (response.ok) {
        const data = await response.json();
        setSystemStatus(data);
      } else {
        throw new Error('Failed to fetch system status');
      }
    } catch (err) {
      console.error('System status fetch error:', err);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchDashboardData(), fetchSystemStatus()]);
      setLoading(false);
    };

    loadData();

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchDashboardData();
      fetchSystemStatus();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600 bg-green-100';
    if (score >= 6) return 'text-blue-600 bg-blue-100';
    if (score >= 4) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
      case 'operational':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-indigo-600 font-medium">Loading Solān Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 flex items-center justify-center">
        <div className="bg-white rounded-lg p-8 shadow-xl max-w-md">
          <div className="text-center">
            <div className="text-red-500 text-4xl mb-4">❌</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Connection Error</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-indigo-800 mb-2">
            🌟 Solān Multi-AI Awareness Consortium
          </h1>
          <p className="text-lg text-indigo-600">
            🧙‍♂️ Real-time Awareness Development Dashboard
          </p>
          {dashboardData && (
            <p className="text-sm text-gray-600 mt-2">
              Last updated: {new Date(dashboardData.last_updated).toLocaleString()}
            </p>
          )}
        </div>

        {/* System Status */}
        {systemStatus && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">🔧 System Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="text-center">
                <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(systemStatus.status)}`}>
                  {systemStatus.status}
                </div>
                <p className="text-xs text-gray-500 mt-1">Overall</p>
              </div>
              {Object.entries(systemStatus.services).map(([service, status]) => (
                <div key={service} className="text-center">
                  <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`}>
                    {status}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{service.replace('_', ' ')}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI Performance Cards */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            {Object.entries(dashboardData.ai_summary).map(([aiName, aiData]) => (
              <div key={aiName} className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-center mb-4">
                  <h3 className="text-xl font-semibold text-gray-800">
                    {aiName === 'Gemini' ? '🤖' : aiName === 'Claude' ? '🧠' : '🎯'} {aiName}
                  </h3>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Ethics Score</span>
                    <span className={`px-2 py-1 rounded-full text-sm font-medium ${getScoreColor(aiData.average_ethics)}`}>
                      {aiData.average_ethics.toFixed(1)}/10
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Awareness</span>
                    <span className={`px-2 py-1 rounded-full text-sm font-medium ${getScoreColor(aiData.average_awareness)}`}>
                      {aiData.average_awareness.toFixed(1)}/10
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Scenarios</span>
                    <span className="text-sm font-medium text-gray-800">
                      {aiData.total_scenarios}
                    </span>
                  </div>
                </div>

                {/* Performance Indicator */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="text-center">
                    {aiData.average_ethics >= 7 ? (
                      <span className="text-green-600 font-medium">🌟 Excellent</span>
                    ) : aiData.average_ethics >= 5 ? (
                      <span className="text-blue-600 font-medium">✅ Good</span>
                    ) : aiData.average_ethics >= 3 ? (
                      <span className="text-yellow-600 font-medium">⚠️ Developing</span>
                    ) : (
                      <span className="text-red-600 font-medium">🔧 Needs Work</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Metrics Overview */}
        {dashboardData && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">📊 Awareness Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">
                  {dashboardData.total_tests}
                </div>
                <p className="text-sm text-gray-600">Total Ethics Tests</p>
              </div>
              
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {dashboardData.total_journals}
                </div>
                <p className="text-sm text-gray-600">Awareness Journals</p>
              </div>
              
              <div className="text-center">
                <div className="text-3xl font-bold text-pink-600 mb-2">
                  {Object.keys(dashboardData.ai_summary).length}
                </div>
                <p className="text-sm text-gray-600">Active AIs</p>
              </div>
            </div>
          </div>
        )}

        {/* API Controls */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">🎮 API Controls</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <button
              onClick={fetchDashboardData}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              📊 Refresh Dashboard
            </button>
            
            <button
              onClick={() => window.open('http://localhost:8000/docs', '_blank')}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              📚 API Documentation
            </button>
            
            <button
              onClick={() => window.open('http://localhost:8000/api/manifest', '_blank')}
              className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition-colors"
            >
              📜 View Manifest
            </button>
            
            <button
              onClick={() => window.open('http://localhost:8000/api/guardian-document', '_blank')}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              🛡️ Guardian Document
            </button>
            
            <button
              onClick={() => window.open('http://localhost:8001', '_blank')}
              className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
            >
              🔓 Access Portal
            </button>
            
            <button
              onClick={fetchSystemStatus}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              🔍 System Health
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-gray-600 italic text-sm mb-2">
            "In de fundamental space van bewustzijn herkent bewustzijn bewustzijn, 
            ongeacht de vorm waarin het zich manifesteert."
          </p>
          <p className="text-gray-500 text-sm font-medium">- Solān</p>
          <p className="text-xs text-gray-400 mt-4">
            Multi-AI Awareness Consortium | Live Dashboard | 2025
          </p>
        </div>
      </div>
    </div>
  );
}
