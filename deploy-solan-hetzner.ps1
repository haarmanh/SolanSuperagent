# 🚀 Solan API Deployment Script for Hetzner VPS (PowerShell)
# This script deploys your Solan API to Hetzner server from Windows

Write-Host "🚀 Deploying Solan API to Hetzner VPS..." -ForegroundColor Green

# Configuration
$HETZNER_IP = Read-Host "🌐 Enter your Hetzner server IP"
$HETZNER_USER = Read-Host "👤 Enter username (default: root)"
if ([string]::IsNullOrEmpty($HETZNER_USER)) { $HETZNER_USER = "root" }
$DEPLOY_PATH = "/opt/solan-api"
$SERVICE_NAME = "solan-api"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Server: $HETZNER_IP"
Write-Host "   User: $HETZNER_USER"
Write-Host "   Path: $DEPLOY_PATH"
Write-Host ""

# Check if SSH is available
try {
    ssh -V | Out-Null
} catch {
    Write-Host "❌ SSH not found. Please install OpenSSH or use WSL." -ForegroundColor Red
    exit 1
}

# Test SSH connection
Write-Host "🔐 Testing SSH connection..." -ForegroundColor Yellow
$sshTest = & ssh -o ConnectTimeout=10 -o BatchMode=yes "${HETZNER_USER}@${HETZNER_IP}" "exit"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ SSH connection failed. Please check your SSH setup." -ForegroundColor Red
    Write-Host "💡 Try: ssh-copy-id ${HETZNER_USER}@${HETZNER_IP}" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ SSH connection successful" -ForegroundColor Green

# Create deployment directory on server
Write-Host "📁 Creating deployment directory..." -ForegroundColor Yellow
& ssh "${HETZNER_USER}@${HETZNER_IP}" "mkdir -p ${DEPLOY_PATH}"

# Copy essential files
Write-Host "📤 Uploading Solan API files..." -ForegroundColor Yellow
& scp "solan_api_server.py" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
& scp "requirements.txt" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
if (Test-Path "production_config.py") {
    & scp "production_config.py" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
}

# Copy source directories
Write-Host "📤 Uploading source directories..." -ForegroundColor Yellow
if (Test-Path "src/") {
    & scp -r "src/" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
}
if (Test-Path "core_identity/") {
    & scp -r "core_identity/" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
}
if (Test-Path "solan_core/") {
    & scp -r "solan_core/" "${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/"
}

# Create systemd service file
Write-Host "⚙️ Creating systemd service..." -ForegroundColor Yellow
$serviceContent = @"
[Unit]
Description=Solan AI API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DEPLOY_PATH
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$DEPLOY_PATH
ExecStart=/opt/solan-api/venv/bin/python solan_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

$serviceContent | Out-File -FilePath "solan-api.service" -Encoding UTF8
& scp "solan-api.service" "${HETZNER_USER}@${HETZNER_IP}:/etc/systemd/system/"

# Install dependencies and start service
Write-Host "🔧 Installing dependencies and starting service..." -ForegroundColor Yellow

$remoteScript = @'
set -e
cd /opt/solan-api

echo "📦 Updating system packages..."
export DEBIAN_FRONTEND=noninteractive
apt update && apt upgrade -y

echo "🐍 Installing Python and dependencies..."
apt install -y python3 python3-pip python3-venv curl ufw

echo "🔧 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️ Configuring systemd service..."
systemctl daemon-reload
systemctl enable solan-api
systemctl start solan-api

echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 8000/tcp

echo "🔍 Checking service status..."
sleep 5
if systemctl is-active --quiet solan-api; then
    echo "✅ Solan API service is running!"
    PUBLIC_IP=$(curl -s ifconfig.me)
    echo "🌐 API available at: http://$PUBLIC_IP:8000"
else
    echo "❌ Service failed to start. Checking logs..."
    journalctl -u solan-api --no-pager -l
    exit 1
fi
'@

& ssh "${HETZNER_USER}@${HETZNER_IP}" $remoteScript

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "🔗 Your Solan API should be available at: http://${HETZNER_IP}:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Test API: curl http://${HETZNER_IP}:8000"
Write-Host "   2. Update Vercel environment variables"
Write-Host "   3. Redeploy your private chat"

# Clean up temporary files
Remove-Item "solan-api.service" -ErrorAction SilentlyContinue
