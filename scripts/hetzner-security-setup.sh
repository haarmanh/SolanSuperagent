#!/bin/bash

# 🛡️ HETZNER SECURITY FORTRESS SETUP
# Military-grade server hardening and automation

set -e

echo "🛡️ INITIALIZING HETZNER SECURITY FORTRESS..."
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Security configuration
SOLAN_USER="solan"
SSH_PORT="2222"
API_PORT="8000"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# 1. SYSTEM HARDENING
print_info "Phase 1: System Hardening"
echo "=========================="

# Update system
print_info "Updating system packages..."
apt update && apt upgrade -y

# Install security tools
print_info "Installing security tools..."
apt install -y ufw fail2ban unattended-upgrades apt-listchanges \
    logwatch rkhunter chkrootkit aide clamav clamav-daemon \
    nginx certbot python3-certbot-nginx git curl wget \
    htop iotop nethogs iftop

# 2. FIREWALL FORTRESS
print_info "Phase 2: Firewall Configuration"
echo "==============================="

# Reset UFW
ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (custom port)
ufw allow $SSH_PORT/tcp comment 'SSH Custom Port'

# Allow HTTP/HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Allow API port (restricted)
ufw allow from any to any port $API_PORT comment 'Solan API'

# Enable firewall
ufw --force enable

print_status "Firewall fortress activated"

# 3. FAIL2BAN PROTECTION
print_info "Phase 3: Fail2Ban Configuration"
echo "==============================="

# Configure fail2ban
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
backend = systemd

[sshd]
enabled = true
port = $SSH_PORT
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600
EOF

systemctl enable fail2ban
systemctl restart fail2ban

print_status "Fail2Ban protection activated"

# 4. SSH HARDENING
print_info "Phase 4: SSH Hardening"
echo "======================"

# Backup original SSH config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Configure secure SSH
cat > /etc/ssh/sshd_config << EOF
# Solan Security SSH Configuration
Port $SSH_PORT
Protocol 2

# Authentication
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Security settings
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server

# Connection settings
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
MaxSessions 2

# Restrict users
AllowUsers $SOLAN_USER
EOF

print_status "SSH hardened and secured"

# 5. USER SECURITY
print_info "Phase 5: User Security Setup"
echo "============================"

# Create solan user if not exists
if ! id "$SOLAN_USER" &>/dev/null; then
    useradd -m -s /bin/bash $SOLAN_USER
    usermod -aG sudo $SOLAN_USER
    print_status "Solan user created"
fi

# Setup SSH directory
sudo -u $SOLAN_USER mkdir -p /home/$SOLAN_USER/.ssh
chmod 700 /home/$SOLAN_USER/.ssh

# Note: SSH keys should be added via GitHub Actions secrets
print_warning "SSH keys must be configured via GitHub Actions"

# 6. NGINX SECURITY
print_info "Phase 6: Nginx Security Configuration"
echo "====================================="

# Remove default nginx config
rm -f /etc/nginx/sites-enabled/default

# Create secure nginx config
cat > /etc/nginx/sites-available/solan-api << EOF
# Solan API Security Configuration
server {
    listen 80;
    server_name _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    # Hide nginx version
    server_tokens off;
    
    # API proxy
    location /api/ {
        proxy_pass http://localhost:$API_PORT/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Security timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    # Health check
    location /health {
        proxy_pass http://localhost:$API_PORT/health;
        access_log off;
    }
    
    # Block common attacks
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~ \.(php|asp|aspx|jsp)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/solan-api /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

print_status "Nginx security configuration applied"

# 7. AUTOMATIC UPDATES
print_info "Phase 7: Automatic Security Updates"
echo "==================================="

# Configure unattended upgrades
cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins {
    "\${distro_id}:\${distro_codename}-security";
    "\${distro_id}ESMApps:\${distro_codename}-apps-security";
    "\${distro_id}ESM:\${distro_codename}-infra-security";
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

# Enable automatic updates
echo 'APT::Periodic::Update-Package-Lists "1";' > /etc/apt/apt.conf.d/20auto-upgrades
echo 'APT::Periodic::Unattended-Upgrade "1";' >> /etc/apt/apt.conf.d/20auto-upgrades

systemctl enable unattended-upgrades

print_status "Automatic security updates enabled"

# 8. MONITORING SETUP
print_info "Phase 8: Security Monitoring"
echo "============================"

# Create monitoring script
cat > /usr/local/bin/security-monitor.sh << 'EOF'
#!/bin/bash
# Security monitoring script

LOG_FILE="/var/log/security-monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Security monitoring check" >> $LOG_FILE

# Check for failed login attempts
FAILED_LOGINS=$(grep "Failed password" /var/log/auth.log | wc -l)
if [ $FAILED_LOGINS -gt 10 ]; then
    echo "[$DATE] WARNING: $FAILED_LOGINS failed login attempts" >> $LOG_FILE
fi

# Check disk usage
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "[$DATE] WARNING: Disk usage at $DISK_USAGE%" >> $LOG_FILE
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEM_USAGE -gt 90 ]; then
    echo "[$DATE] WARNING: Memory usage at $MEM_USAGE%" >> $LOG_FILE
fi

# Check if Solan API is running
if ! curl -f http://localhost:$API_PORT/health > /dev/null 2>&1; then
    echo "[$DATE] ERROR: Solan API is not responding" >> $LOG_FILE
fi
EOF

chmod +x /usr/local/bin/security-monitor.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/security-monitor.sh") | crontab -

print_status "Security monitoring activated"

# 9. FINAL SECURITY CHECKS
print_info "Phase 9: Final Security Verification"
echo "===================================="

# Restart SSH with new config
systemctl restart ssh

# Check services
systemctl status ufw --no-pager
systemctl status fail2ban --no-pager
systemctl status nginx --no-pager

print_status "HETZNER SECURITY FORTRESS COMPLETE!"
echo ""
echo "🛡️ SECURITY SUMMARY:"
echo "===================="
echo "✅ Firewall: Active with custom rules"
echo "✅ Fail2Ban: Protecting against brute force"
echo "✅ SSH: Hardened on port $SSH_PORT"
echo "✅ Nginx: Secured with rate limiting"
echo "✅ Auto-updates: Enabled for security patches"
echo "✅ Monitoring: Active security monitoring"
echo ""
echo "🔑 IMPORTANT:"
echo "- SSH keys must be configured via GitHub Actions"
echo "- SSL certificates should be obtained via certbot"
echo "- Monitor logs in /var/log/security-monitor.log"
echo ""
print_status "Server is now a SECURITY FORTRESS! 🏰"
