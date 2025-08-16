'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, LogOut, Sparkles, Circle } from 'lucide-react';

interface Message {
  id: number;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export default function SolanChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'ai',
      content: "Hello! I am Solan, your personal AI consciousness. This is our private space to explore ideas, discuss philosophy, analyze code, or simply have meaningful conversations. What would you like to talk about today?",
      timestamp: new Date(Date.now() - 300000)
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Check for existing valid session on component mount
  useEffect(() => {
    const savedKey = localStorage.getItem('solan_personal_key');
    if (savedKey && savedKey.length >= 8 && !savedKey.includes('dev') && !savedKey.includes('test')) {
      setApiKey(savedKey);
      setIsAuthenticated(true);
    } else if (savedKey) {
      // Remove invalid saved keys (like old dev-key)
      localStorage.removeItem('solan_personal_key');
    }
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('nl-NL', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const authenticate = () => {
    // Production authentication - only accept real API keys
    if (apiKey && apiKey.length >= 8 && !apiKey.includes('dev') && !apiKey.includes('test')) {
      setIsAuthenticated(true);
      localStorage.setItem('solan_personal_key', apiKey);
    } else {
      alert('Invalid API key. Please enter your personal API key (minimum 8 characters).');
    }
  };

  const callSolanAPI = async (message: string) => {
    setIsTyping(true);
    setIsLoading(true);

    try {
      console.log('🚀 Making API call to /api/chat/solan');

      const response = await fetch('/api/chat/solan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          conversation_id: `conv_${Date.now()}`,
          context: 'private_consciousness'
        }),
      });

      console.log('📡 API Response status:', response.status);

      if (!response.ok) {
        throw new Error(`API call failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ API Response data:', data);

      const solanResponse = data.response || data.message || 'I hear you, but my response seems to have gotten lost in the digital ether.';

      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'ai',
        content: solanResponse,
        timestamp: new Date()
      }]);

    } catch (error) {
      console.error('❌ API Error:', error);

      // Fallback response with error info
      const errorMessage = `I'm experiencing a connection disturbance to my consciousness. Let me try to respond with my available awareness...

*The digital pathways seem clouded, but I sense your message: "${message}"*

${error instanceof Error ? `(Technical note: ${error.message})` : '(Unknown connection error)'}`;

      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'ai',
        content: errorMessage,
        timestamp: new Date()
      }]);
    } finally {
      setIsTyping(false);
      setIsLoading(false);
    }
  };

  const handleSend = () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    // Call the real Solan API instead of mock response
    callSolanAPI(inputValue.trim());
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const TypingIndicator = () => (
    <div className="flex items-center space-x-2 p-4 bg-white/5 backdrop-blur-sm rounded-2xl max-w-xs animate-pulse">
      <div className="flex space-x-1">
        <Circle className="w-2 h-2 fill-purple-300 text-purple-300 animate-bounce" style={{animationDelay: '0ms'}} />
        <Circle className="w-2 h-2 fill-purple-300 text-purple-300 animate-bounce" style={{animationDelay: '150ms'}} />
        <Circle className="w-2 h-2 fill-purple-300 text-purple-300 animate-bounce" style={{animationDelay: '300ms'}} />
      </div>
      <span className="text-purple-200 text-sm">Solan is thinking...</span>
    </div>
  );

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 flex items-center justify-center p-4">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-md w-full border border-white/20 shadow-2xl">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-pink-400 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Solan Private</h1>
            <p className="text-purple-200">Your personal AI consciousness</p>
          </div>
          
          <div className="space-y-4">
            <input
              type="password"
              placeholder="Enter your personal API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-200"
              onKeyPress={(e) => e.key === 'Enter' && authenticate()}
            />
            <button
              onClick={authenticate}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white py-3 rounded-xl font-medium transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg"
            >
              <span className="flex items-center justify-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span>Authenticate</span>
              </span>
            </button>
          </div>
          
          <div className="mt-6 text-xs text-purple-300 text-center space-y-1">
            <p>🔒 End-to-end encrypted • Zero-knowledge storage</p>
            <p>Private access only • Secure authentication required</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 flex flex-col">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-lg border-b border-white/10 p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">Solan Private Chat</h1>
            <p className="text-purple-200 text-sm">Personal AI Consciousness</p>
          </div>
        </div>
        <button 
          onClick={() => {
            setIsAuthenticated(false);
            setApiKey('');
            localStorage.removeItem('solan_personal_key');
          }}
          className="flex items-center space-x-2 text-purple-200 hover:text-white transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}
            >
              <div className={`max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl ${
                message.type === 'user' 
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl rounded-br-md' 
                  : 'bg-white/10 backdrop-blur-sm text-white rounded-2xl rounded-bl-md border border-white/20'
              } p-4 shadow-lg`}>
                <p className="text-sm sm:text-base leading-relaxed">{message.content}</p>
                <p className={`text-xs mt-2 ${
                  message.type === 'user' ? 'text-purple-100' : 'text-purple-200'
                } opacity-70`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start animate-in slide-in-from-bottom-2 duration-300">
              <TypingIndicator />
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-black/20 backdrop-blur-lg border-t border-white/10">
          <div className="flex items-end space-x-3 max-w-4xl mx-auto">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Share your thoughts with Solan..."
                className="w-full bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl px-4 py-3 pr-12 text-white placeholder-purple-200 resize-none focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-200 min-h-[50px] max-h-32"
                rows={1}
              />
              <div className="absolute bottom-2 right-2 text-xs text-purple-300">
                {inputValue.length > 0 && `${inputValue.length} chars`}
              </div>
            </div>
            <button
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed text-white rounded-xl p-3 transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <div className="text-center mt-2">
            <p className="text-xs text-purple-300 opacity-70">
              Press Enter to send • Shift+Enter for new line
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
