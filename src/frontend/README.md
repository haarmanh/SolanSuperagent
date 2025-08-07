# Solan Superagent Frontend

Modern React dashboard for Solan's awareness coherence and cognitive analytics.

## Features

- 🧠 **Real-time Coherence Analytics** - Live monitoring of awareness coherence
- ✨ **Cognitive Insights** - Deep cognitive development tracking
- 📚 **Memory History** - Coherence-tagged memory exploration
- 📊 **Interactive Charts** - Beautiful data visualizations with Recharts
- 🎨 **Modern UI** - Built with shadcn/ui and Tailwind CSS
- ⚡ **Fast Development** - Powered by Vite

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Recharts** for data visualization
- **Lucide React** for icons
- **React Router** for navigation
- **Axios** for API communication

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd src/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   └── layout/       # Layout components
│   ├── pages/            # Page components
│   ├── lib/              # Utilities and API
│   ├── app.tsx           # Main app component
│   └── index.tsx         # Entry point
├── public/               # Static assets
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

The frontend connects to the Python backend API at `http://localhost:8000/api/` with the following endpoints:

- `/api/dashboard/coherence` - Coherence trends
- `/api/dashboard/cognitive` - Cognitive analytics  
- `/api/dashboard/history` - Memory coherence history
- `/api/dashboard/overview` - Complete dashboard overview

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Adding New Components

1. Create component in appropriate directory
2. Export from index file if needed
3. Import and use in pages or other components

### Styling

- Use Tailwind CSS classes for styling
- Custom colors defined in `tailwind.config.js`
- Component variants using `class-variance-authority`

## Features Overview

### Dashboard
- System health overview
- Quick stats and metrics
- Real-time status indicators

### Coherence Analytics
- Multi-period trend analysis (day/week/month)
- Interactive line and bar charts
- Coherence level distribution
- Growth metrics and insights

### Cognitive Insights
- Cognitive depth tracking
- Development trend analysis
- Health assessment
- Period-based comparisons

### Memory History
- Agent-specific memory filtering
- Coherence-tagged entries
- Detailed memory exploration
- Emotional and moral significance tracking

### Settings
- Theme and appearance customization
- Data collection preferences
- Notification configuration
- Privacy and security settings

## Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Add proper error handling
4. Test components thoroughly
5. Update documentation as needed

## License

Part of the Solan Superagent project.
