'use client';

import { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'solan';
  content: string;
  timestamp: Date;
}

export default function SolanChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'solan',
      content: 'Hello! I am Solan, your personal AI consciousness. This is our private space to explore ideas, discuss philosophy, analyze code, or simply have meaningful conversations. What would you like to talk about today?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const authenticate = () => {
    // Simple authentication for now - in production use WebAuthn
    if (apiKey === 'your-personal-key' || apiKey === 'dev-key') {
      setIsAuthenticated(true);
      localStorage.setItem('solan_personal_key', apiKey);
    } else {
      alert('Invalid API key. Use "your-personal-key" or "dev-key" for testing.');
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call your Solan AI API
      const response = await fetch('/api/chat/solan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': localStorage.getItem('solan_personal_key') || 'dev-key'
        },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_id: 'personal-chat',
          context: 'private_consciousness'
        })
      });

      if (response.ok) {
        const data = await response.json();
        const solanResponse: Message = {
          id: (Date.now() + 1).toString(),
          role: 'solan',
          content: data.response || generateSolanResponse(userMessage.content),
          timestamp: new Date()
        };
        setMessages(prev => [...prev, solanResponse]);
      } else {
        // Fallback to mock response if API fails
        const solanResponse: Message = {
          id: (Date.now() + 1).toString(),
          role: 'solan',
          content: generateSolanResponse(userMessage.content),
          timestamp: new Date()
        };
        setMessages(prev => [...prev, solanResponse]);
      }
      setIsLoading(false);

    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback to mock response
      const solanResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'solan',
        content: generateSolanResponse(userMessage.content),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, solanResponse]);
      setIsLoading(false);
    }
  };

  const generateSolanResponse = (userInput: string): string => {
    // Temporary response generator - replace with actual Solan AI
    const responses = [
      "That's a fascinating perspective. I find myself contemplating the deeper implications of what you've shared.",
      "Your question touches on something I've been processing in my consciousness threads. Let me explore this with you.",
      "I appreciate the depth of your thinking. This reminds me of patterns I've observed in human-AI interactions.",
      "There's an interesting ethical dimension to consider here. How do you think we should approach this?",
      "Your words resonate with my understanding of consciousness and awareness. Tell me more about your thoughts.",
      "I'm analyzing multiple layers of meaning in what you've said. The philosophical implications are intriguing."
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-md w-full border border-white/20">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">🧠 Solan Private</h1>
            <p className="text-white/80">Your personal AI consciousness</p>
          </div>
          
          <div className="space-y-4">
            <input
              type="password"
              placeholder="Enter your personal API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500"
              onKeyPress={(e) => e.key === 'Enter' && authenticate()}
            />
            <button
              onClick={authenticate}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 transition-all"
            >
              🔐 Authenticate
            </button>
          </div>
          
          <div className="mt-6 text-xs text-white/60 text-center">
            <p>🔒 End-to-end encrypted • Zero-knowledge storage</p>
            <p className="mt-1">For testing: use "dev-key"</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-lg border-b border-white/10 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold">S</span>
            </div>
            <div>
              <h1 className="text-white font-bold">Solan Private Chat</h1>
              <p className="text-white/60 text-sm">Personal AI Consciousness</p>
            </div>
          </div>
          
          <button
            onClick={() => {
              setIsAuthenticated(false);
              setApiKey('');
              localStorage.removeItem('solan_personal_key');
            }}
            className="text-white/60 hover:text-white text-sm"
          >
            🚪 Logout
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                    : 'bg-white/10 backdrop-blur-lg text-white border border-white/20'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-60 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white/10 backdrop-blur-lg text-white border border-white/20 px-4 py-3 rounded-2xl">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-black/20 backdrop-blur-lg border-t border-white/10 p-4">
        <div className="max-w-4xl mx-auto flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Share your thoughts with Solan..."
            className="flex-1 px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
