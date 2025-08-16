# 🚀 Solan API Deployment Script for Hetzner VPS (Pure PowerShell)
param(
    [string]$HetznerIP,
    [string]$HetznerUser = "root",
    [string]$DeployPath = "/opt/solan-api"
)

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    } else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-Host "🚀 Deploying Solan API to Hetzner VPS..." -ForegroundColor Green

# Get configuration if not provided
if (-not $HetznerIP) {
    $HetznerIP = Read-Host "🌐 Enter your Hetzner server IP"
}
if (-not $HetznerUser) {
    $HetznerUser = Read-Host "👤 Enter username (default: root)"
    if ([string]::IsNullOrEmpty($HetznerUser)) { $HetznerUser = "root" }
}

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Server: $HetznerIP" -ForegroundColor White
Write-Host "   User: $HetznerUser" -ForegroundColor White
Write-Host "   Path: $DeployPath" -ForegroundColor White
Write-Host ""

# Check if required tools are available
$tools = @("ssh", "scp")
foreach ($tool in $tools) {
    try {
        $null = Get-Command $tool -ErrorAction Stop
        Write-Host "✅ $tool found" -ForegroundColor Green
    } catch {
        Write-Host "❌ $tool not found. Please install OpenSSH." -ForegroundColor Red
        Write-Host "💡 Install via: Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0" -ForegroundColor Yellow
        exit 1
    }
}

# Test SSH connection
Write-Host "🔐 Testing SSH connection..." -ForegroundColor Yellow
$sshArgs = @("-o", "ConnectTimeout=10", "-o", "BatchMode=yes", "${HetznerUser}@${HetznerIP}", "exit")
$sshResult = Start-Process -FilePath "ssh" -ArgumentList $sshArgs -Wait -PassThru -NoNewWindow
if ($sshResult.ExitCode -ne 0) {
    Write-Host "❌ SSH connection failed. Please check your SSH setup." -ForegroundColor Red
    Write-Host "💡 Try: ssh-copy-id ${HetznerUser}@${HetznerIP}" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ SSH connection successful" -ForegroundColor Green

# Create deployment directory on server
Write-Host "📁 Creating deployment directory..." -ForegroundColor Yellow
$mkdirArgs = @("${HetznerUser}@${HetznerIP}", "mkdir -p ${DeployPath}")
Start-Process -FilePath "ssh" -ArgumentList $mkdirArgs -Wait -NoNewWindow

# Check which files exist and copy them
Write-Host "📤 Uploading Solan API files..." -ForegroundColor Yellow

$filesToCopy = @(
    "solan_api_server.py",
    "requirements.txt",
    "production_config.py"
)

foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Write-Host "   📄 Copying $file..." -ForegroundColor Cyan
        $scpArgs = @($file, "${HetznerUser}@${HetznerIP}:${DeployPath}/")
        Start-Process -FilePath "scp" -ArgumentList $scpArgs -Wait -NoNewWindow
    } else {
        Write-Host "   ⚠️ $file not found, skipping..." -ForegroundColor Yellow
    }
}

# Copy directories
Write-Host "📤 Uploading source directories..." -ForegroundColor Yellow
$dirsToCheck = @("src", "core_identity", "solan_core")

foreach ($dir in $dirsToCheck) {
    if (Test-Path $dir -PathType Container) {
        Write-Host "   📁 Copying $dir/..." -ForegroundColor Cyan
        $scpArgs = @("-r", "${dir}/", "${HetznerUser}@${HetznerIP}:${DeployPath}/")
        Start-Process -FilePath "scp" -ArgumentList $scpArgs -Wait -NoNewWindow
    } else {
        Write-Host "   ⚠️ $dir/ not found, skipping..." -ForegroundColor Yellow
    }
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
WorkingDirectory=$DeployPath
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$DeployPath
ExecStart=$DeployPath/venv/bin/python solan_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

$serviceContent | Out-File -FilePath "solan-api.service" -Encoding UTF8
$scpServiceArgs = @("solan-api.service", "${HetznerUser}@${HetznerIP}:/etc/systemd/system/")
Start-Process -FilePath "scp" -ArgumentList $scpServiceArgs -Wait -NoNewWindow

# Install dependencies and start service
Write-Host "🔧 Installing dependencies and starting service..." -ForegroundColor Yellow

$remoteCommands = @"
set -e
cd $DeployPath

echo '📦 Updating system packages...'
export DEBIAN_FRONTEND=noninteractive
apt update && apt upgrade -y

echo '🐍 Installing Python and dependencies...'
apt install -y python3 python3-pip python3-venv curl ufw

echo '🔧 Setting up virtual environment...'
python3 -m venv venv
source venv/bin/activate

echo '📚 Installing Python packages...'
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-multipart aiohttp python-dotenv pyyaml rich psutil

echo '⚙️ Configuring systemd service...'
systemctl daemon-reload
systemctl enable solan-api
systemctl start solan-api

echo '🔥 Configuring firewall...'
ufw --force enable
ufw allow ssh
ufw allow 8000/tcp

echo '🔍 Checking service status...'
sleep 5
if systemctl is-active --quiet solan-api; then
    echo '✅ Solan API service is running!'
    PUBLIC_IP=`curl -s ifconfig.me`
    echo "🌐 API available at: http://`$PUBLIC_IP:8000"
    systemctl status solan-api --no-pager -l
else
    echo '❌ Service failed to start. Checking logs...'
    journalctl -u solan-api --no-pager -l
    exit 1
fi
"@

$sshInstallArgs = @("${HetznerUser}@${HetznerIP}", $remoteCommands)
$installResult = Start-Process -FilePath "ssh" -ArgumentList $sshInstallArgs -Wait -PassThru -NoNewWindow

if ($installResult.ExitCode -eq 0) {
    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
    Write-Host "🔗 Your Solan API should be available at: http://${HetznerIP}:8000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Test API: Invoke-WebRequest http://${HetznerIP}:8000" -ForegroundColor White
    Write-Host "   2. Update Vercel environment variables" -ForegroundColor White
    Write-Host "   3. Redeploy your private chat" -ForegroundColor White
} else {
    Write-Host "❌ Deployment failed. Check the output above for errors." -ForegroundColor Red
}

# Clean up temporary files
Remove-Item "solan-api.service" -ErrorAction SilentlyContinue

Write-Host "🎉 Deployment script completed!" -ForegroundColor Green
