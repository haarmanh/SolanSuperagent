# 🚀 Clean Solan API Deployment to Hetzner VPS
# Pure PowerShell - No mixed syntax

param(
    [string]$ServerIP,
    [string]$Username = "root"
)

function Write-Step {
    param([string]$Message, [string]$Color = "Yellow")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Main deployment function
function Deploy-SolanToHetzner {
    Write-Host "🚀 Solan API Hetzner Deployment" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""

    # Get server details if not provided
    if (-not $ServerIP) {
        $ServerIP = Read-Host "🌐 Enter your Hetzner server IP address"
    }
    if (-not $Username) {
        $Username = Read-Host "👤 Enter username (press Enter for 'root')"
        if ([string]::IsNullOrEmpty($Username)) { $Username = "root" }
    }

    Write-Host "📋 Configuration:" -ForegroundColor Yellow
    Write-Host "   Server: $ServerIP"
    Write-Host "   User: $Username"
    Write-Host "   Deploy Path: /opt/solan-api"
    Write-Host ""

    # Check prerequisites
    Write-Step "🔍 Checking prerequisites..."
    
    if (-not (Test-Command "ssh")) {
        Write-Error "SSH not found. Install OpenSSH client first."
        Write-Host "💡 Run: Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0" -ForegroundColor Yellow
        return $false
    }
    
    if (-not (Test-Command "scp")) {
        Write-Error "SCP not found. Install OpenSSH client first."
        return $false
    }

    Write-Success "Prerequisites OK"

    # Test SSH connection
    Write-Step "🔐 Testing SSH connection..."
    $testConnection = Start-Process -FilePath "ssh" -ArgumentList @("-o", "ConnectTimeout=10", "-o", "BatchMode=yes", "$Username@$ServerIP", "echo 'Connection OK'") -Wait -PassThru -WindowStyle Hidden
    
    if ($testConnection.ExitCode -ne 0) {
        Write-Error "SSH connection failed"
        Write-Host "💡 Make sure you can SSH to your server: ssh $Username@$ServerIP" -ForegroundColor Yellow
        return $false
    }
    Write-Success "SSH connection working"

    # Create remote directory
    Write-Step "📁 Creating deployment directory..."
    $createDir = Start-Process -FilePath "ssh" -ArgumentList @("$Username@$ServerIP", "mkdir -p /opt/solan-api") -Wait -PassThru -WindowStyle Hidden
    if ($createDir.ExitCode -eq 0) {
        Write-Success "Directory created"
    } else {
        Write-Error "Failed to create directory"
        return $false
    }

    # Upload files
    Write-Step "📤 Uploading files..."
    
    $filesToUpload = @(
        "solan_api_server.py",
        "requirements.txt"
    )

    foreach ($file in $filesToUpload) {
        if (Test-Path $file) {
            Write-Host "   📄 Uploading $file..." -ForegroundColor Cyan
            $upload = Start-Process -FilePath "scp" -ArgumentList @($file, "$Username@${ServerIP}:/opt/solan-api/") -Wait -PassThru -WindowStyle Hidden
            if ($upload.ExitCode -eq 0) {
                Write-Host "   ✅ $file uploaded" -ForegroundColor Green
            } else {
                Write-Error "Failed to upload $file"
                return $false
            }
        } else {
            Write-Host "   ⚠️ $file not found, skipping" -ForegroundColor Yellow
        }
    }

    # Upload directories
    $dirsToUpload = @("src", "core_identity", "solan_core")
    foreach ($dir in $dirsToUpload) {
        if (Test-Path $dir -PathType Container) {
            Write-Host "   📁 Uploading $dir/..." -ForegroundColor Cyan
            $uploadDir = Start-Process -FilePath "scp" -ArgumentList @("-r", "$dir/", "$Username@${ServerIP}:/opt/solan-api/") -Wait -PassThru -WindowStyle Hidden
            if ($uploadDir.ExitCode -eq 0) {
                Write-Host "   ✅ $dir/ uploaded" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️ Failed to upload $dir/, continuing..." -ForegroundColor Yellow
            }
        } else {
            Write-Host "   ⚠️ $dir/ not found, skipping" -ForegroundColor Yellow
        }
    }

    # Create systemd service file locally
    Write-Step "⚙️ Creating service configuration..."
    $serviceContent = @"
[Unit]
Description=Solan AI API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/solan-api
Environment=PATH=/opt/solan-api/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=/opt/solan-api
ExecStart=/opt/solan-api/venv/bin/python solan_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

    $serviceContent | Out-File -FilePath "solan-api.service" -Encoding UTF8 -NoNewline
    
    # Upload service file
    $uploadService = Start-Process -FilePath "scp" -ArgumentList @("solan-api.service", "$Username@${ServerIP}:/etc/systemd/system/") -Wait -PassThru -WindowStyle Hidden
    if ($uploadService.ExitCode -eq 0) {
        Write-Success "Service file uploaded"
    } else {
        Write-Error "Failed to upload service file"
        return $false
    }

    # Install and configure on server
    Write-Step "🔧 Installing dependencies and configuring server..."
    
    $setupScript = @"
set -e
cd /opt/solan-api
echo 'Updating system...'
export DEBIAN_FRONTEND=noninteractive
apt update && apt upgrade -y
echo 'Installing Python...'
apt install -y python3 python3-pip python3-venv curl ufw
echo 'Creating virtual environment...'
python3 -m venv venv
source venv/bin/activate
echo 'Installing Python packages...'
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-multipart aiohttp python-dotenv pyyaml rich psutil
echo 'Configuring service...'
systemctl daemon-reload
systemctl enable solan-api
systemctl start solan-api
echo 'Configuring firewall...'
ufw --force enable
ufw allow ssh
ufw allow 8000/tcp
echo 'Checking service...'
sleep 3
if systemctl is-active --quiet solan-api; then
    echo 'SUCCESS: Solan API is running!'
    PUBLIC_IP=`curl -s ifconfig.me`
    echo "API URL: http://`$PUBLIC_IP:8000"
else
    echo 'ERROR: Service failed to start'
    journalctl -u solan-api --no-pager -l
    exit 1
fi
"@

    $setupResult = Start-Process -FilePath "ssh" -ArgumentList @("$Username@$ServerIP", $setupScript) -Wait -PassThru -NoNewWindow
    
    if ($setupResult.ExitCode -eq 0) {
        Write-Success "Server setup completed!"
        Write-Host ""
        Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
        Write-Host "🌐 Your Solan API is running at: http://$ServerIP:8000" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📋 Next steps:" -ForegroundColor Yellow
        Write-Host "   1. Test: Invoke-WebRequest http://$ServerIP:8000" -ForegroundColor White
        Write-Host "   2. Update Vercel env vars: SOLAN_BACKEND_URL=http://$ServerIP:8000" -ForegroundColor White
        Write-Host "   3. Redeploy your private chat" -ForegroundColor White
    } else {
        Write-Error "Server setup failed. Check the output above."
        return $false
    }

    # Cleanup
    Remove-Item "solan-api.service" -ErrorAction SilentlyContinue
    return $true
}

# Run deployment
Deploy-SolanToHetzner
