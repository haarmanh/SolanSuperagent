#!/bin/bash

# 🚀 Simple Solan API Deployment to Hetzner VPS
# Works in WSL, Linux, or Mac

set -e  # Exit on any error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Solan API Hetzner Deployment${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Get server details
read -p "🌐 Enter your Hetzner server IP: " SERVER_IP
read -p "👤 Enter username (default: root): " USERNAME
USERNAME=${USERNAME:-root}

DEPLOY_PATH="/opt/solan-api"

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "   Server: $SERVER_IP"
echo "   User: $USERNAME"
echo "   Deploy Path: $DEPLOY_PATH"
echo ""

# Check prerequisites
echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"

if ! command -v ssh &> /dev/null; then
    echo -e "${RED}❌ SSH not found${NC}"
    exit 1
fi

if ! command -v scp &> /dev/null; then
    echo -e "${RED}❌ SCP not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"

# Test SSH connection
echo -e "${YELLOW}🔐 Testing SSH connection...${NC}"
if ssh -o ConnectTimeout=10 -o BatchMode=yes $USERNAME@$SERVER_IP exit; then
    echo -e "${GREEN}✅ SSH connection working${NC}"
else
    echo -e "${RED}❌ SSH connection failed${NC}"
    echo -e "${YELLOW}💡 Make sure you can SSH to your server: ssh $USERNAME@$SERVER_IP${NC}"
    exit 1
fi

# Create remote directory
echo -e "${YELLOW}📁 Creating deployment directory...${NC}"
ssh $USERNAME@$SERVER_IP "mkdir -p $DEPLOY_PATH"
echo -e "${GREEN}✅ Directory created${NC}"

# Upload files
echo -e "${YELLOW}📤 Uploading files...${NC}"

FILES_TO_UPLOAD=(
    "solan_api_server.py"
    "requirements.txt"
)

for file in "${FILES_TO_UPLOAD[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   📄 Uploading $file..."
        scp "$file" $USERNAME@$SERVER_IP:$DEPLOY_PATH/
        echo -e "${GREEN}   ✅ $file uploaded${NC}"
    else
        echo -e "${YELLOW}   ⚠️ $file not found, skipping${NC}"
    fi
done

# Upload directories
DIRS_TO_UPLOAD=("src" "core_identity" "solan_core")

for dir in "${DIRS_TO_UPLOAD[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "   📁 Uploading $dir/..."
        scp -r "$dir/" $USERNAME@$SERVER_IP:$DEPLOY_PATH/
        echo -e "${GREEN}   ✅ $dir/ uploaded${NC}"
    else
        echo -e "${YELLOW}   ⚠️ $dir/ not found, skipping${NC}"
    fi
done

# Create systemd service file
echo -e "${YELLOW}⚙️ Creating service configuration...${NC}"
cat > solan-api.service << EOF
[Unit]
Description=Solan AI API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DEPLOY_PATH
Environment=PATH=$DEPLOY_PATH/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$DEPLOY_PATH
ExecStart=$DEPLOY_PATH/venv/bin/python solan_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Upload service file
scp solan-api.service $USERNAME@$SERVER_IP:/etc/systemd/system/
echo -e "${GREEN}✅ Service file uploaded${NC}"

# Install and configure on server
echo -e "${YELLOW}🔧 Installing dependencies and configuring server...${NC}"

ssh $USERNAME@$SERVER_IP << 'REMOTE_SCRIPT'
set -e
cd /opt/solan-api

echo "📦 Updating system..."
export DEBIAN_FRONTEND=noninteractive
apt update && apt upgrade -y

echo "🐍 Installing Python..."
apt install -y python3 python3-pip python3-venv curl ufw

echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-multipart aiohttp python-dotenv pyyaml rich psutil

echo "⚙️ Configuring service..."
systemctl daemon-reload
systemctl enable solan-api
systemctl start solan-api

echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 8000/tcp

echo "🔍 Checking service..."
sleep 3
if systemctl is-active --quiet solan-api; then
    echo "✅ SUCCESS: Solan API is running!"
    PUBLIC_IP=$(curl -s ifconfig.me)
    echo "🌐 API URL: http://$PUBLIC_IP:8000"
    echo ""
    echo "📊 Service status:"
    systemctl status solan-api --no-pager -l
else
    echo "❌ ERROR: Service failed to start"
    echo "📋 Checking logs:"
    journalctl -u solan-api --no-pager -l
    exit 1
fi
REMOTE_SCRIPT

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL!${NC}"
    echo -e "${CYAN}🌐 Your Solan API is running at: http://$SERVER_IP:8000${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "   1. Test: curl http://$SERVER_IP:8000"
    echo "   2. Update Vercel env vars: SOLAN_BACKEND_URL=http://$SERVER_IP:8000"
    echo "   3. Redeploy your private chat"
else
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Cleanup
rm -f solan-api.service

echo -e "${GREEN}🎉 Deployment script completed!${NC}"
