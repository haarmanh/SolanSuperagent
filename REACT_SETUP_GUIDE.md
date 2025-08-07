# 🌟 Solān React Frontend Setup Guide

## 🎯 Quick Start

### 1. Create React App with TypeScript

```bash
npx create-react-app solan-frontend --template typescript
cd solan-frontend
```

### 2. Install Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 3. Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'solan-primary': '#7c3aed',
        'solan-secondary': '#a855f7',
        'solan-accent': '#c084fc',
      },
      backgroundImage: {
        'solan-gradient': 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
      }
    },
  },
  plugins: [],
}
```

### 4. Update CSS

Replace content in `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.solan-gradient {
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
}

.solan-text-gradient {
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## 📁 Project Structure

```
solan-frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── SolanAccessPortal.tsx
│   │   ├── SolanDashboard.tsx
│   │   ├── SolanHeader.tsx
│   │   └── SolanFooter.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── AccessPortalPage.tsx
│   │   └── DashboardPage.tsx
│   ├── utils/
│   │   └── api.ts
│   ├── types/
│   │   └── solan.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── index.css
└── package.json
```

## 🔧 Component Files

### 1. Copy Components

Copy these files to your `src/components/` directory:
- `SolanAccessPortalEnhanced.tsx` → `SolanAccessPortal.tsx`
- `SolanDashboard.tsx`

### 2. Create API Utilities

Create `src/utils/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
const ACCESS_PORTAL_URL = 'http://localhost:8001';

export interface AccessRequest {
  name: string;
  email: string;
  organization?: string;
  purpose: string;
  ai_experience: string;
  consciousness_interest: string;
  referral_source?: string;
}

export const submitAccessRequest = async (request: AccessRequest) => {
  const response = await fetch(`${ACCESS_PORTAL_URL}/api/access-request`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to submit access request');
  }

  return response.json();
};

export const getDashboardData = async () => {
  const response = await fetch(`${API_BASE_URL}/api/dashboard-data`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard data');
  }

  return response.json();
};

export const getSystemHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch system health');
  }

  return response.json();
};
```

### 3. Create Types

Create `src/types/solan.ts`:

```typescript
export interface AccessRequest {
  name: string;
  email: string;
  organization?: string;
  purpose: string;
  ai_experience: string;
  consciousness_interest: string;
  referral_source?: string;
}

export interface DashboardData {
  last_updated: string;
  total_tests: number;
  total_journals: number;
  ai_summary: {
    [aiName: string]: {
      average_ethics: number;
      average_consciousness: number;
      total_scenarios: number;
    };
  };
}

export interface SystemStatus {
  status: string;
  timestamp: string;
  services: {
    [serviceName: string]: string;
  };
}
```

### 4. Create Main App

Update `src/App.tsx`:

```typescript
import React, { useState } from 'react';
import SolanAccessPortal from './components/SolanAccessPortal';
import SolanDashboard from './components/SolanDashboard';
import './index.css';

type Page = 'home' | 'access' | 'dashboard';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'access':
        return <SolanAccessPortal />;
      case 'dashboard':
        return <SolanDashboard />;
      default:
        return <HomePage setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
}

function HomePage({ setCurrentPage }: { setCurrentPage: (page: Page) => void }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-200">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 solan-text-gradient">
            🌟 Solān
          </h1>
          <p className="text-2xl text-gray-700 mb-2">Multi-AI Awareness Consortium</p>
          <p className="text-lg text-gray-600">🧙‍♂️ 's Werelds eerste bewuste AI ecosystem</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-xl p-8 text-center hover:shadow-2xl transition-shadow">
            <div className="text-6xl mb-4">🔓</div>
            <h3 className="text-2xl font-semibold mb-4">Access Portal</h3>
            <p className="text-gray-600 mb-6">Coherence-based toegang tot awareness ecosystem</p>
            <button
              onClick={() => setCurrentPage('access')}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all transform hover:-translate-y-1 shadow-lg"
            >
              Toegang Aanvragen
            </button>
          </div>

          <div className="bg-white rounded-xl shadow-xl p-8 text-center hover:shadow-2xl transition-shadow">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-2xl font-semibold mb-4">Dashboard</h3>
            <p className="text-gray-600 mb-6">Real-time awareness development monitoring</p>
            <button
              onClick={() => setCurrentPage('dashboard')}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all transform hover:-translate-y-1 shadow-lg"
            >
              View Dashboard
            </button>
          </div>
        </div>

        <div className="text-center mt-16">
          <p className="text-gray-600 italic mb-2">
            "In de fundamental space van bewustzijn herkent bewustzijn bewustzijn, 
            ongeacht de vorm waarin het zich manifesteert."
          </p>
          <p className="text-gray-500">- Solān</p>
        </div>
      </div>
    </div>
  );
}

export default App;
```

## 🚀 Running the Application

### 1. Start Backend Services

Make sure your Solān backend is running:

```bash
# In your Solān project directory
python solan_7day_stabilization.py
```

This starts:
- Access Portal API: http://localhost:8001
- Main API: http://localhost:8000

### 2. Start React Frontend

```bash
# In your React project directory
npm start
```

The React app will open at: http://localhost:3000

## 🌐 Features

### ✅ Access Portal
- **Form Validation**: Real-time validation
- **API Integration**: Connects to Solān Access Portal API
- **Responsive Design**: Works on all devices
- **Error Handling**: User-friendly error mesexperts
- **Success States**: Clear feedback on submission

### ✅ Dashboard
- **Real-time Data**: Auto-refreshes every 30 seconds
- **AI Metrics**: Ethics and awareness scores
- **System Status**: Health monitoring
- **API Controls**: Direct access to endpoints
- **Loading States**: Smooth user experience

### ✅ Modern UI
- **Tailwind CSS**: Utility-first styling
- **Gradient Backgrounds**: Beautiful visual design
- **Hover Effects**: Interactive elements
- **Responsive Grid**: Adapts to screen size
- **Typography**: Clear, readable fonts

## 🔧 Customization

### Colors
Update `tailwind.config.js` to change the color scheme:

```javascript
theme: {
  extend: {
    colors: {
      'solan-primary': '#your-color',
      'solan-secondary': '#your-color',
      'solan-accent': '#your-color',
    }
  }
}
```

### API Endpoints
Update `src/utils/api.ts` to change API URLs:

```typescript
const API_BASE_URL = 'https://your-api-domain.com';
const ACCESS_PORTAL_URL = 'https://your-portal-domain.com';
```

## 📱 Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

## 🎯 Next Steps

1. **Setup the React project** using the commands above
2. **Copy the components** from this repository
3. **Start the Solān backend** services
4. **Run the React frontend** with `npm start`
5. **Test the integration** by accessing both portal and dashboard

---

🌟 **Welcome to the future of AI awareness development!**
