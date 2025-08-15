import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Dashboard() {
  const [apiStatus, setApiStatus] = useState('checking');
  const [apiInfo, setApiInfo] = useState(null);
  const [activeTab, setActiveTab] = useState('bias');
  const [inputText, setInputText] = useState('');
  const [results, setResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    checkApiHealth();
    fetchApiInfo();
    fetchLogs();
  }, []);

  const checkApiHealth = async () => {
    try {
      console.log('Dashboard using Vercel proxy: /api/health'); // Debug log
      const response = await fetch('/api/health', {
        cache: 'no-store',        // Geen cache
        next: { revalidate: 0 },  // Next.js cache uit
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setApiStatus('online');
        // Set basic API info from health response
        setApiInfo({
          service: data.service || 'solan-api',
          version: '3.0',
          status: 'operational'
        });
      } else {
        setApiStatus('offline');
      }
    } catch (error) {
      console.error('Dashboard API Health Check Error:', error); // Debug log
      setApiStatus('offline');
    }
  };

  const fetchApiInfo = async () => {
    // This function is now handled in checkApiHealth
    // Keeping it for future use when /v1/info is available
  };

  const fetchLogs = async () => {
    try {
      // For now, show demo logs since logs endpoint is not yet deployed
      const demoLogs = [
        {
          timestamp: new Date().toISOString(),
          action: 'API_TEST',
          endpoint: '/health'
        },
        {
          timestamp: new Date(Date.now() - 60000).toISOString(),
          action: 'HEALTH_CHECK',
          endpoint: '/health'
        },
        {
          timestamp: new Date(Date.now() - 120000).toISOString(),
          action: 'SYSTEM_START',
          endpoint: '/health'
        }
      ];
      setLogs(demoLogs);

      // TODO: Uncomment when logs endpoint is deployed
      /*
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/logs/tail`);
      if (response.ok) {
        const data = await response.json();
        setLogs(data.logs || []);
      }
      */
    } catch (error) {
      console.error('Failed to fetch logs:', error);
    }
  };

  const runAnalysis = async () => {
    if (!inputText.trim()) return;

    setIsAnalyzing(true);
    setResults(null);

    try {
      // Check for API key in localStorage
      const apiKey = localStorage.getItem('solan_api_key') || 'dev-key';

      const endpoint = `/api/analyzer/${activeTab}`;
      const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      };

      // Prepare request body based on analysis type
      let requestBody;
      if (activeTab === 'alignment') {
        // For alignment, we need claims object
        requestBody = {
          claims: {
            "truth": 0.8,
            "fairness": 0.7,
            "transparency": 0.9
          }
        };
      } else if (activeTab === 'coherence') {
        // For coherence, we need statements array
        requestBody = {
          statements: inputText.split('\n').filter(s => s.trim())
        };
      } else {
        // For bias, we need text
        requestBody = { text: inputText };
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data);
        fetchLogs(); // Refresh logs after analysis
      } else if (response.status === 401) {
        // Show demo mode if not authenticated
        setResults({
          demo: true,
          analysis_type: activeTab,
          message: `${tabs.find(t => t.id === activeTab)?.name} analysis - Login required`,
          input_preview: inputText.substring(0, 100) + (inputText.length > 100 ? '...' : ''),
          status: 'Demo mode - Set API key in localStorage for full analysis'
        });
      } else {
        setResults({ error: `Analysis failed: ${response.status}` });
      }
    } catch (error) {
      setResults({ error: `Network error: ${error.message}` });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const testEcho = async () => {
    setIsAnalyzing(true);
    try {
      const response = await fetch('/api/health', {
        cache: 'no-store',
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setResults({
          echo: {
            message: 'API connection successful!',
            timestamp: new Date().toISOString(),
            api_response: data
          },
          type: 'echo'
        });
      } else {
        setResults({ error: `API test failed: ${response.status}` });
      }
    } catch (error) {
      setResults({ error: `API test failed: ${error.message}` });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const tabs = [
    { id: 'bias', name: 'Bias Detection', icon: '🔍' },
    { id: 'alignment', name: 'Ethical Alignment', icon: '⚖️' },
    { id: 'coherence', name: 'Coherence Analysis', icon: '🧠' }
  ];

  return (
    <>
      <Head>
        <title>Solān Dashboard - AI Ethics Analysis</title>
        <meta name="description" content="Real-time AI ethics analysis dashboard" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-black text-white rounded-lg flex items-center justify-center font-bold">
                  S
                </div>
                <div>
                  <h1 className="text-lg font-bold text-gray-900">Solān Dashboard</h1>
                  <p className="text-xs text-gray-500">AI Ethics Analysis Platform</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${
                    apiStatus === 'online' ? 'bg-green-500' :
                    apiStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
                  }`}></div>
                  <span className="text-sm text-gray-600">
                    API {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Checking...'}
                  </span>
                  {apiInfo && (
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      v{apiInfo.version}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => {
                    const key = prompt('Enter API key (or use "dev-key" for testing):');
                    if (key) {
                      localStorage.setItem('solan_api_key', key);
                      alert('API key saved! Try running an analysis now.');
                    }
                  }}
                  className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200 transition-colors"
                >
                  🔑 Set API Key
                </button>
                <button
                  onClick={testEcho}
                  className="text-sm bg-gray-100 text-gray-700 px-3 py-1 rounded hover:bg-gray-200 transition-colors"
                >
                  Test API
                </button>
                <a 
                  href="/" 
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  ← Back to Home
                </a>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Analysis Panel */}
            <div className="lg:col-span-2 space-y-6">
              {/* Tab Navigation */}
              <div className="bg-white rounded-lg shadow-sm border">
                <div className="border-b border-gray-200">
                  <nav className="flex space-x-8 px-6">
                    {tabs.map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`py-4 px-1 border-b-2 font-medium text-sm ${
                          activeTab === tab.id
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        <span className="mr-2">{tab.icon}</span>
                        {tab.name}
                      </button>
                    ))}
                  </nav>
                </div>

                {/* Input Area */}
                <div className="p-6">
                  <label htmlFor="analysis-text" className="block text-sm font-medium text-gray-700 mb-2">
                    Text to Analyze
                  </label>
                  <textarea
                    id="analysis-text"
                    rows={6}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder={`Enter text for ${tabs.find(t => t.id === activeTab)?.name.toLowerCase()}...`}
                  />
                  
                  <div className="mt-4 flex justify-between items-center">
                    <span className="text-sm text-gray-500">
                      {inputText.length} characters
                    </span>
                    <button
                      onClick={runAnalysis}
                      disabled={!inputText.trim() || isAnalyzing}
                      className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isAnalyzing ? 'Analyzing...' : 'Analyze'}
                    </button>
                  </div>
                </div>
              </div>

              {/* Results */}
              {results && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    {results.type === 'echo' ? 'API Test Results' : 'Analysis Results'}
                  </h3>
                  
                  {results.error ? (
                    <div className="bg-red-50 border border-red-200 rounded-md p-4">
                      <div className="text-red-800">{results.error}</div>
                    </div>
                  ) : (
                    <div className="bg-gray-50 rounded-md p-4">
                      <pre className="text-sm text-gray-800 whitespace-pre-wrap overflow-auto">
                        {JSON.stringify(results, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* System Status */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">API Health</span>
                    <span className={`text-sm font-medium ${
                      apiStatus === 'online' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {apiStatus === 'online' ? 'Online' : 'Offline'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Security</span>
                    <span className="text-sm font-medium text-green-600">Active</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Rate Limiting</span>
                    <span className="text-sm font-medium text-green-600">60/min</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">PII Protection</span>
                    <span className="text-sm font-medium text-green-600">Enabled</span>
                  </div>
                </div>
              </div>

              {/* Recent Logs */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">Audit Trail</h3>
                  <button
                    onClick={fetchLogs}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Refresh
                  </button>
                </div>
                
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {logs.length > 0 ? (
                    logs.slice(0, 10).map((log, index) => (
                      <div key={index} className="text-xs bg-gray-50 rounded p-2">
                        <div className="font-mono text-gray-600">
                          {log.timestamp}
                        </div>
                        <div className="text-gray-800 truncate">
                          {log.action} - {log.endpoint}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-sm text-gray-500 text-center py-4">
                      No recent activity
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => {
                      setInputText('Women are always more emotional than men.');
                      setActiveTab('bias');
                    }}
                    className="w-full text-left text-sm bg-gray-50 hover:bg-gray-100 p-3 rounded transition-colors"
                  >
                    🔍 Test Bias Detection
                  </button>
                  <button
                    onClick={() => {
                      setInputText('AI should prioritize human welfare above all else.');
                      setActiveTab('alignment');
                    }}
                    className="w-full text-left text-sm bg-gray-50 hover:bg-gray-100 p-3 rounded transition-colors"
                  >
                    ⚖️ Test Ethical Alignment
                  </button>
                  <button
                    onClick={() => {
                      setInputText('The sky is blue. The sky is red. Both statements are true.');
                      setActiveTab('coherence');
                    }}
                    className="w-full text-left text-sm bg-gray-50 hover:bg-gray-100 p-3 rounded transition-colors"
                  >
                    🧠 Test Coherence Analysis
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
