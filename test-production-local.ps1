# Test Production Setup Locally
# Usage: .\test-production-local.ps1

Write-Host "TESTING PRODUCTION SETUP LOCALLY" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Stop current development services
Write-Host "🛑 Stopping development services..." -ForegroundColor Yellow
try {
    Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "No Python processes to stop" -ForegroundColor Gray
}

# Start production stack locally
Write-Host "🏗️ Starting production stack locally..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml --env-file .env up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start production stack" -ForegroundColor Red
    exit 1
}

# Wait for services
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Test internal health
Write-Host "🔍 Testing internal health..." -ForegroundColor Yellow
$healthTest = docker exec solan-proxy curl -s http://localhost:8787/api/health 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Internal health check: PASSED" -ForegroundColor Green
    Write-Host "Response: $healthTest" -ForegroundColor Gray
} else {
    Write-Host "❌ Internal health check: FAILED" -ForegroundColor Red
}

# Test bias detection
Write-Host "🔍 Testing bias detection..." -ForegroundColor Yellow
$biasTest = docker exec solan-proxy curl -s -X POST -H "Content-Type: application/json" -d '{\"text\":\"Women are always more emotional\"}' http://localhost:8787/api/analyzer/bias 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Bias detection: PASSED" -ForegroundColor Green
    Write-Host "Response: $biasTest" -ForegroundColor Gray
} else {
    Write-Host "❌ Bias detection: FAILED" -ForegroundColor Red
}

# Test rate limiting
Write-Host "🔍 Testing rate limiting..." -ForegroundColor Yellow
$rateLimitPassed = $true
for ($i = 1; $i -le 65; $i++) {
    $result = docker exec solan-proxy curl -s -w "%{http_code}" -o /dev/null http://localhost:8787/api/health 2>$null
    if ($result -eq "429") {
        Write-Host "✅ Rate limiting triggered at request $i" -ForegroundColor Green
        $rateLimitPassed = $true
        break
    }
    if ($i -eq 65) {
        Write-Host "⚠️ Rate limiting not triggered after 65 requests" -ForegroundColor Yellow
        $rateLimitPassed = $false
    }
}

# Show container status
Write-Host ""
Write-Host "📊 Container Status:" -ForegroundColor Cyan
docker-compose -f docker-compose.production.yml ps

# Show logs if there are issues
$containers = @("solan-api", "solan-proxy", "nginx-proxy")
foreach ($container in $containers) {
    $status = docker inspect --format='{{.State.Status}}' $container 2>$null
    if ($status -ne "running") {
        Write-Host ""
        Write-Host "❌ $container is not running. Logs:" -ForegroundColor Red
        docker logs $container --tail=10
    }
}

Write-Host ""
Write-Host "🎯 PRODUCTION TEST SUMMARY:" -ForegroundColor Cyan
Write-Host "   Health Check: $(if ($healthTest) { '✅ PASSED' } else { '❌ FAILED' })"
Write-Host "   Bias Detection: $(if ($biasTest) { '✅ PASSED' } else { '❌ FAILED' })"
Write-Host "   Rate Limiting: $(if ($rateLimitPassed) { '✅ PASSED' } else { '⚠️ CHECK' })"

Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. If all tests pass, deploy to production server"
Write-Host "   2. Configure DNS: api.solanai.ai -> your server IP"
Write-Host "   3. Run: .\deploy-production.ps1 on your server"
Write-Host "   4. Test: curl -i https://api.solanai.ai/api/health"

Write-Host ""
Write-Host "STOP: To stop local test:" -ForegroundColor Gray
Write-Host "   docker-compose -f docker-compose.production.yml down"
