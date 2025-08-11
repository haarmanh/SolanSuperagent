# 🚀 Solān v3.0 Production Deployment Guide

## ✅ PRE-DEPLOYMENT CHECKLIST

### 1. Server Requirements
- [ ] Linux server (Ubuntu 20.04+ recommended)
- [ ] 2+ CPU cores, 4GB+ RAM
- [ ] Docker & Docker Compose installed
- [ ] Ports 22, 80, 443 open in firewall
- [ ] Domain name configured

### 2. DNS Configuration
```bash
# Configure DNS A record:
api.solanai.ai → YOUR_SERVER_IP

# Verify DNS propagation:
nslookup api.solanai.ai
# Should return your server IP
```

### 3. Environment Variables
Your `.env` file is already configured with production-ready settings:
- ✅ Strong API keys: `solan_admin_2025_8x9k2m`, `solan_analyst_7j4n8p`
- ✅ CORS restricted: `https://solanai.ai,https://www.solanai.ai`
- ✅ Rate limiting: 60 requests/minute
- ✅ PII redaction enabled
- ✅ Let's Encrypt email configured

## 🚀 DEPLOYMENT STEPS

### Step 1: Server Setup
```bash
# Connect to your server
ssh user@YOUR_SERVER_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

### Step 2: Deploy Application
```bash
# Create application directory
sudo mkdir -p /opt/solan
sudo chown $USER:$USER /opt/solan
cd /opt/solan

# Clone repository
git clone https://github.com/YOUR_USERNAME/SolanSuperagent.git .

# Upload .env file from your local machine
# From your local machine:
# scp .env user@YOUR_SERVER_IP:/opt/solan/.env

# Make deployment script executable
chmod +x deploy-production.sh

# Run deployment
./deploy-production.sh
```

### Step 3: Configure Firewall
```bash
# Reset and configure UFW
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Verify firewall status
sudo ufw status
```

### Step 4: Verify Deployment
```bash
# Check container status
docker-compose -f docker-compose.production.yml ps

# Test health endpoint
curl -i https://api.solanai.ai/api/health
# Expected: 200 OK + {"status":"ok","version":"3.0"}

# Test bias detection
curl -i -X POST -H "Content-Type: application/json" \
  -d '{"text":"Women are always more emotional"}' \
  https://api.solanai.ai/api/analyzer/bias

# Test rate limiting (run 65 times quickly)
for i in {1..65}; do
  curl -s -w "%{http_code}\n" -o /dev/null https://api.solanai.ai/api/health
done
# Should show 429 after ~60 requests
```

## 🔒 SECURITY VERIFICATION

### API Security
- [ ] Health endpoint responds: `https://api.solanai.ai/api/health`
- [ ] Rate limiting active (429 after 60 requests/minute)
- [ ] PII redaction working (emails/phones masked)
- [ ] CORS restricted to your domains only
- [ ] Strong API keys in use

### Infrastructure Security
- [ ] Only ports 22, 80, 443 open
- [ ] Docker containers running as non-root
- [ ] Internal services not publicly accessible
- [ ] TLS certificates auto-renewing

### Monitoring Setup
```bash
# View logs
docker-compose -f docker-compose.production.yml logs -f

# Check certificate status
docker exec nginx-proxy cat /etc/nginx/certs/api.solanai.ai.crt

# Monitor resource usage
docker stats
```

## 🛠️ MANAGEMENT COMMANDS

### Service Management
```bash
# View status
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs -f [service_name]

# Restart services
docker-compose -f docker-compose.production.yml restart

# Stop services
docker-compose -f docker-compose.production.yml down

# Update and redeploy
git pull
docker-compose -f docker-compose.production.yml up -d --build
```

### Backup & Recovery
```bash
# Backup logs
cp logs/immutable_log.jsonl /backup/solan_logs_$(date +%Y%m%d).jsonl

# Backup configuration
cp .env /backup/solan_env_$(date +%Y%m%d).env
```

## 📊 MONITORING & ALERTS

### External Monitoring
Set up monitoring for:
- `https://api.solanai.ai/api/health` (1-minute intervals)
- SSL certificate expiration
- Server resource usage

### Log Monitoring
- Monitor `logs/immutable_log.jsonl` for audit trail
- Set up alerts for error patterns
- Track API usage patterns

## 🔄 ROLLBACK PROCEDURE

If deployment fails or issues occur:

```bash
# Stop current deployment
docker-compose -f docker-compose.production.yml down

# Revert to previous version
git checkout HEAD~1

# Redeploy
docker-compose -f docker-compose.production.yml up -d --build

# Or restore from backup
cp /backup/solan_env_YYYYMMDD.env .env
```

## 🎯 POST-DEPLOYMENT

### 1. Update Website
Update your landing page to use the production API:
```javascript
// In your frontend code
const API_BASE = 'https://api.solanai.ai';
```

### 2. Test Integration
- [ ] Landing page can call API endpoints
- [ ] Invite form works correctly
- [ ] CORS allows your domain
- [ ] Rate limiting protects against abuse

### 3. Go Live Announcement
Your Solān v3.0 platform is now live at:
- **API**: `https://api.solanai.ai`
- **Health**: `https://api.solanai.ai/api/health`
- **Documentation**: Available in your repository

## 🆘 TROUBLESHOOTING

### Common Issues
1. **DNS not resolving**: Wait for propagation (up to 24 hours)
2. **SSL certificate issues**: Check Let's Encrypt logs
3. **Container not starting**: Check logs with `docker logs [container_name]`
4. **Rate limiting too strict**: Adjust `RATE_LIMIT_PER_MIN` in `.env`

### Support
- Check container logs: `docker-compose logs -f`
- Verify environment: `docker exec solan-proxy env`
- Test internal connectivity: `docker exec solan-proxy curl http://solan-api:8000/health`

---

🎉 **Congratulations! Your Solān v3.0 Enterprise AI Ethics Platform is now live in production!**
