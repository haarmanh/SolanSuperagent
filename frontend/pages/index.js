import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Home() {
  const [apiStatus, setApiStatus] = useState('checking');
  const [inviteForm, setInviteForm] = useState({
    name: '',
    email: '',
    org: '',
    role: '',
    reason: ''
  });
  const [inviteStatus, setInviteStatus] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Check API health on load
  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  const checkApiHealth = async () => {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'https://api.solanai.ai';
      console.log('API Base URL:', apiBase); // Debug log
      const response = await fetch(`${apiBase}/health`);
      if (response.ok) {
        setApiStatus('online');
      } else {
        setApiStatus('offline');
      }
    } catch (error) {
      console.error('API Health Check Error:', error); // Debug log
      setApiStatus('offline');
    }
  };

  const handleInviteSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setInviteStatus('');

    try {
      const response = await fetch('/api/invite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inviteForm)
      });

      const data = await response.json();

      if (response.ok) {
        setInviteStatus('success');
        setInviteForm({ name: '', email: '', org: '', role: '', reason: '' });
      } else {
        setInviteStatus(`error: ${data.message || 'Something went wrong'}`);
      }
    } catch (error) {
      setInviteStatus('error: Network error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (e) => {
    setInviteForm({
      ...inviteForm,
      [e.target.name]: e.target.value
    });
  };

  return (
    <>
      <Head>
        <title>Solān v3.0 — AI Ethics, Security & Bias Detection</title>
        <meta name="description" content="Enterprise-grade AI Analysis Platform with bias detection, ethical alignment scoring, and immutable audit trails." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-black text-white rounded-xl flex items-center justify-center font-bold text-lg">
                  S
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Solān Labs</h1>
                  <p className="text-sm text-gray-500">AI Ethics • Security • Analysis</p>
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
                </div>
                <a
                  href="/observatorium"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  Observatorium
                </a>
                <a
                  href="/dashboard"
                  className="bg-black text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors"
                >
                  Dashboard
                </a>
              </div>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              AI Ethics Platform
              <span className="block text-blue-600">for Enterprises</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Enterprise-grade AI Analysis Platform with bias detection, ethical alignment scoring, 
              coherence analysis and immutable audit trails. Now in closed beta.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="#invite" 
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Request Beta Access
              </a>
              <a 
                href="#features" 
                className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg hover:bg-gray-50 transition-colors font-medium"
              >
                View Features
              </a>
            </div>
          </div>

          {/* Features Grid */}
          <section id="features" className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="bg-white p-8 rounded-2xl shadow-sm border">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Bias Detection</h3>
              <p className="text-gray-600">
                Advanced pattern detection with benchmark linkage and explainability. 
                Transparent thresholds and clear limitations.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-sm border">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Ethical Alignment</h3>
              <p className="text-gray-600">
                Scoring mapped to NIST AI RMF, OECD, and ISO frameworks. 
                Includes detailed reasoning for each score.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-sm border">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Coherence Analysis</h3>
              <p className="text-gray-600">
                Detects inconsistencies, contradictions and temporal breaks 
                in AI model outputs with high precision.
              </p>
            </div>
          </section>

          {/* Stats */}
          <section className="bg-white rounded-2xl shadow-sm border p-8 mb-16">
            <div className="grid md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold text-gray-900">99.9%</div>
                <div className="text-gray-600">Uptime</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-gray-900">&lt;200ms</div>
                <div className="text-gray-600">Response Time</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-gray-900">Enterprise</div>
                <div className="text-gray-600">Security</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-gray-900">GDPR</div>
                <div className="text-gray-600">Compliant</div>
              </div>
            </div>
          </section>

          {/* Invite Form */}
          <section id="invite" className="bg-white rounded-2xl shadow-sm border p-8">
            <div className="max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Join the Closed Beta
              </h3>
              <p className="text-gray-600 text-center mb-8">
                Get early access to our enterprise AI ethics platform. 
                We'll respond within 2 business days.
              </p>

              <form onSubmit={handleInviteSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                      Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      value={inviteForm.name}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      value={inviteForm.email}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="org" className="block text-sm font-medium text-gray-700 mb-2">
                      Organization
                    </label>
                    <input
                      type="text"
                      id="org"
                      name="org"
                      value={inviteForm.org}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                      Role
                    </label>
                    <input
                      type="text"
                      id="role"
                      name="role"
                      value={inviteForm.role}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-2">
                    Why are you interested? *
                  </label>
                  <textarea
                    id="reason"
                    name="reason"
                    required
                    rows={4}
                    value={inviteForm.reason}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Tell us about your use case..."
                  />
                </div>

                <div className="text-center">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? 'Submitting...' : 'Request Access'}
                  </button>
                  
                  {inviteStatus && (
                    <div className={`mt-4 p-3 rounded-lg ${
                      inviteStatus === 'success' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {inviteStatus === 'success' 
                        ? 'Thank you! We\'ll be in touch soon.' 
                        : inviteStatus}
                    </div>
                  )}
                </div>
              </form>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-gray-600">
              <p>&copy; 2025 Solān Labs. All rights reserved.</p>
              <p className="mt-2 text-sm">
                Enterprise AI Ethics Platform • GDPR Compliant • SOC 2 Ready
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
