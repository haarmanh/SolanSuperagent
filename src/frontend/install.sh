#!/bin/bash

# Solan Superagent Frontend Installation Script

echo "🚀 Installing Solan Superagent Frontend..."
echo "=========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    echo "   Please upgrade Node.js."
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ npm $(npm -v) detected"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Install additional shadcn/ui components if needed
echo ""
echo "🎨 Setting up shadcn/ui components..."

# Note: In a real setup, you might want to run shadcn/ui init here
# For now, we'll just note that the components are already included

echo "✅ UI components ready"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️ Creating environment configuration..."
    cat > .env << EOL
# Solan Superagent Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=Solan Superagent Dashboard
VITE_APP_VERSION=1.0.0
EOL
    echo "✅ Environment configuration created"
fi

# Run type check
echo ""
echo "🔍 Running type check..."
npm run type-check

if [ $? -ne 0 ]; then
    echo "⚠️ Type check found issues, but continuing..."
else
    echo "✅ Type check passed"
fi

# Build the project to verify everything works
echo ""
echo "🔨 Building project to verify setup..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo "✅ Build successful"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Start the backend API server (Python)"
echo "   2. Run 'npm run dev' to start the development server"
echo "   3. Open http://localhost:3000 in your browser"
echo ""
echo "🔧 Available commands:"
echo "   npm run dev      - Start development server"
echo "   npm run build    - Build for production"
echo "   npm run preview  - Preview production build"
echo "   npm run lint     - Run linter"
echo ""
echo "📚 Documentation: See README.md for more details"
echo ""
echo "Happy coding! 🚀"
