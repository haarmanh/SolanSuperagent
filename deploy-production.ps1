# Solān v3.0 Production Deployment Script (PowerShell)
# Usage: .\deploy-production.ps1

Write-Host "🚀 SOLĀN v3.0 PRODUCTION DEPLOYMENT" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose is not available. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found. Please create it first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites check passed" -ForegroundColor Green

# Load environment variables from .env file
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Validate required environment variables
$requiredVars = @("SOLAN_API_KEYS", "SOLAN_ANALYST_KEY", "SOLAN_ADMIN_KEY", "ALLOW_ORIGINS", "LETSENCRYPT_EMAIL")
foreach ($var in $requiredVars) {
    if (-not [Environment]::GetEnvironmentVariable($var)) {
        Write-Host "❌ Required environment variable $var is not set" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Environment variables validated" -ForegroundColor Green

# Build private chat first
Write-Host ""
Write-Host "🏗️ Building private chat..." -ForegroundColor Cyan
Set-Location solan-private-chat
npm install
npm run build
Set-Location ..

Write-Host "✅ Environment variables validated" -ForegroundColor Green

# Check DNS resolution
Write-Host "🌐 Checking DNS resolution for api.solanai.ai..." -ForegroundColor Yellow
try {
    $null = Resolve-DnsName api.solanai.ai -ErrorAction Stop
    Write-Host "✅ DNS resolution successful" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Warning: DNS for api.solanai.ai not resolved. Make sure DNS is configured." -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
try {
    docker-compose -f docker-compose.production.yml down --remove-orphans
} catch {
    Write-Host "No existing containers to stop" -ForegroundColor Gray
}

# Build and start production stack
Write-Host "🏗️ Building and starting production stack..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file .env up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start production stack" -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Health check
Write-Host "🔍 Performing health checks..." -ForegroundColor Yellow
$maxAttempts = 10
$attempt = 1

while ($attempt -le $maxAttempts) {
    Write-Host "Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    
    # Check internal health first
    try {
        $result = docker exec solan-proxy curl -f http://localhost:8787/api/health 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Internal health check passed" -ForegroundColor Green
            break
        }
    } catch {
        # Continue to next attempt
    }
    
    if ($attempt -eq $maxAttempts) {
        Write-Host "❌ Health check failed after $maxAttempts attempts" -ForegroundColor Red
        Write-Host "📋 Container logs:" -ForegroundColor Yellow
        docker-compose -f docker-compose.production.yml logs --tail=20
        exit 1
    }
    
    Start-Sleep -Seconds 10
    $attempt++
}

# Show deployment status
Write-Host ""
Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml ps

Write-Host ""
Write-Host "🌐 Endpoints:" -ForegroundColor Cyan
Write-Host "   Health: https://api.solanai.ai/api/health"
Write-Host "   Bias:   https://api.solanai.ai/api/analyzer/bias"
Write-Host "   Align:  https://api.solanai.ai/api/analyzer/alignment"
Write-Host "   Logs:   https://api.solanai.ai/api/logs/tail"

Write-Host ""
Write-Host "🔧 Management Commands:" -ForegroundColor Cyan
Write-Host "   View logs:    docker-compose -f docker-compose.production.yml logs -f"
Write-Host "   Stop:         docker-compose -f docker-compose.production.yml down"
Write-Host "   Restart:      docker-compose -f docker-compose.production.yml restart"

Write-Host ""
Write-Host "🧪 Test deployment:" -ForegroundColor Cyan
Write-Host "   curl -i https://api.solanai.ai/api/health"

Write-Host ""
Write-Host "🚀 Solān v3.0 is now LIVE in production!" -ForegroundColor Green
