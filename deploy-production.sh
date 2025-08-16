#!/bin/bash

# Solān v3.0 Production Deployment Script
# Usage: ./deploy-production.sh

set -e  # Exit on any error

echo "🚀 SOLĀN v3.0 PRODUCTION DEPLOYMENT"
echo "=================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Don't run this script as root for security reasons"
   exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Load environment variables
source .env

# Validate required environment variables
required_vars=("SOLAN_API_KEYS" "SOLAN_ANALYST_KEY" "SOLAN_ADMIN_KEY" "ALLOW_ORIGINS" "LETSENCRYPT_EMAIL")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Check DNS resolution
echo "🌐 Checking DNS resolution for api.solanai.ai..."
if ! nslookup api.solanai.ai > /dev/null 2>&1; then
    echo "⚠️ Warning: DNS for api.solanai.ai not resolved. Make sure DNS is configured."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ DNS resolution successful"
fi

# Setup firewall (UFW)
echo "🔒 Setting up firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw --force reset
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow OpenSSH
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    echo "✅ Firewall configured (only SSH, HTTP, HTTPS allowed)"
else
    echo "⚠️ UFW not found. Please configure firewall manually."
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.production.yml down --remove-orphans || true

# Build and start production stack
echo "🏗️ Building and starting production stack..."
docker-compose -f docker-compose.production.yml --env-file .env up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Performing health checks..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt/$max_attempts..."
    
    # Check internal health first
    if docker exec solan-proxy curl -f http://localhost:8787/api/health > /dev/null 2>&1; then
        echo "✅ Internal health check passed"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ Health check failed after $max_attempts attempts"
        echo "📋 Container logs:"
        docker-compose -f docker-compose.production.yml logs --tail=20
        exit 1
    fi
    
    sleep 10
    ((attempt++))
done

# Show deployment status
echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "========================"
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.production.yml ps

echo ""
echo "🌐 Endpoints:"
echo "   Health: https://api.solanai.ai/api/health"
echo "   Bias:   https://api.solanai.ai/api/analyzer/bias"
echo "   Align:  https://api.solanai.ai/api/analyzer/alignment"
echo "   Logs:   https://api.solanai.ai/api/logs/tail"

echo ""
echo "🔧 Management Commands:"
echo "   View logs:    docker-compose -f docker-compose.production.yml logs -f"
echo "   Stop:         docker-compose -f docker-compose.production.yml down"
echo "   Restart:      docker-compose -f docker-compose.production.yml restart"

echo ""
echo "🧪 Test deployment:"
echo "   curl -i https://api.solanai.ai/api/health"

echo ""
echo "🚀 Solān v3.0 is now LIVE in production!"
