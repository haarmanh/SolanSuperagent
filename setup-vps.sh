#!/bin/bash

# Solān VPS Setup Script for Hetzner CX11
# Run this on your fresh Ubuntu 22.04 server

set -e

echo "🚀 SOLĀN VPS SETUP - HETZNER CX11"
echo "================================="

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install essential packages
echo "🔧 Installing essential packages..."
apt install -y curl wget git ufw htop nano

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
echo "🔗 Installing Docker Compose..."
apt install -y docker-compose-plugin

# Configure firewall
echo "🔒 Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Create solan user
echo "👤 Creating solan user..."
useradd -m -s /bin/bash solan
usermod -aG docker solan

# Create application directory
echo "📁 Setting up application directory..."
mkdir -p /opt/solan
chown solan:solan /opt/solan

# Switch to solan user for app setup
echo "🔄 Switching to solan user..."
sudo -u solan bash << 'EOF'
cd /opt/solan

# Clone repository (you'll need to update this URL)
echo "📥 Cloning Solān repository..."
git clone https://github.com/YOUR_USERNAME/SolanSuperagent.git .

# Create logs directory
mkdir -p logs
chmod 755 logs

echo "✅ Application setup complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Upload your .env file: scp .env root@YOUR_SERVER_IP:/opt/solan/.env"
echo "2. Update repository URL in this script"
echo "3. Run deployment: ./deploy-production.sh"
EOF

echo ""
echo "🎉 VPS SETUP COMPLETE!"
echo "====================="
echo ""
echo "📊 Server Info:"
echo "   OS: $(lsb_release -d | cut -f2)"
echo "   Docker: $(docker --version)"
echo "   Firewall: $(ufw status | head -1)"
echo ""
echo "🔧 Next Steps:"
echo "1. Update the GitHub repository URL in this script"
echo "2. Upload your .env file from local machine"
echo "3. Run the deployment script"
echo ""
echo "📝 Commands to run next:"
echo "   scp .env root@YOUR_SERVER_IP:/opt/solan/.env"
echo "   ssh root@YOUR_SERVER_IP"
echo "   cd /opt/solan && ./deploy-production.sh"
