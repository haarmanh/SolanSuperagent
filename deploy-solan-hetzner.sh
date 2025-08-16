#!/bin/bash

# 🚀 Solan API Deployment Script for Hetzner VPS
# This script deploys your Solan API to Hetzner server

echo "🚀 Deploying Solan API to Hetzner VPS..."

# Configuration - UPDATE THESE VALUES
read -p "🌐 Enter your Hetzner server IP: " HETZNER_IP
read -p "👤 Enter username (default: root): " HETZNER_USER
HETZNER_USER=${HETZNER_USER:-root}
DEPLOY_PATH="/opt/solan-api"
SERVICE_NAME="solan-api"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo -e "   Server: ${HETZNER_IP}"
echo -e "   User: ${HETZNER_USER}"
echo -e "   Path: ${DEPLOY_PATH}"
echo ""

# Check if SSH key exists or offer to create one
if [ ! -f ~/.ssh/id_rsa ] && [ ! -f ~/.ssh/id_ed25519 ]; then
    echo -e "${YELLOW}🔑 No SSH key found. Creating one...${NC}"
    read -p "📧 Enter your email for SSH key: " EMAIL
    ssh-keygen -t ed25519 -C "$EMAIL" -f ~/.ssh/id_ed25519 -N ""
    echo -e "${GREEN}✅ SSH key created${NC}"
    echo -e "${YELLOW}📋 Please add this public key to your Hetzner server:${NC}"
    cat ~/.ssh/id_ed25519.pub
    read -p "Press Enter after adding the key to your server..."
fi

# Test SSH connection
echo -e "${YELLOW}🔐 Testing SSH connection...${NC}"
ssh -o ConnectTimeout=10 -o BatchMode=yes ${HETZNER_USER}@${HETZNER_IP} exit
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ SSH connection failed. Please check your SSH setup.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ SSH connection successful${NC}"

# Create deployment directory on server
echo -e "${YELLOW}📁 Creating deployment directory...${NC}"
ssh ${HETZNER_USER}@${HETZNER_IP} "mkdir -p ${DEPLOY_PATH}"

# Copy essential files
echo -e "${YELLOW}📤 Uploading Solan API files...${NC}"
scp solan_api_server.py ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/
scp requirements.txt ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/
scp production_config.py ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/

# Copy source directories
echo -e "${YELLOW}📤 Uploading source directories...${NC}"
scp -r src/ ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/
scp -r core_identity/ ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/
scp -r solan_core/ ${HETZNER_USER}@${HETZNER_IP}:${DEPLOY_PATH}/

# Create systemd service file
echo -e "${YELLOW}⚙️ Creating systemd service...${NC}"
cat > solan-api.service << EOF
[Unit]
Description=Solan AI API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${DEPLOY_PATH}
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=${DEPLOY_PATH}
ExecStart=/usr/bin/python3 solan_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

scp solan-api.service ${HETZNER_USER}@${HETZNER_IP}:/etc/systemd/system/

# Install dependencies and start service
echo -e "${YELLOW}🔧 Installing dependencies and starting service...${NC}"
ssh ${HETZNER_USER}@${HETZNER_IP} << 'ENDSSH'
set -e  # Exit on any error

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
    echo "📊 Service status:"
    systemctl status solan-api --no-pager -l
else
    echo "❌ Service failed to start. Checking logs..."
    journalctl -u solan-api --no-pager -l
    exit 1
fi
ENDSSH

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${YELLOW}🔗 Your Solan API should be available at: http://${HETZNER_IP}:8000${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "   1. Test API: curl http://${HETZNER_IP}:8000"
echo -e "   2. Update Vercel environment variables"
echo -e "   3. Redeploy your private chat"
