# 🚀 Solān v3.0 - Vercel + VPS Deployment Guide

## 🎯 ARCHITECTURE OVERVIEW

```
┌─────────────────┐    ┌─────────────────┐
│   VERCEL        │    │   HETZNER VPS   │
│   (Frontend)    │    │   (Backend)     │
├─────────────────┤    ├─────────────────┤
│ solanai.ai      │◄──►│ api.solanai.ai  │
│ Landing Page    │    │ Solān API       │
│ Observatorium   │    │ Secure Proxy    │
│ /api/invite     │    │ Docker Stack    │
│ Auto-deploy     │    │ Immutable Logs  │
└─────────────────┘    └─────────────────┘
```

## 📋 STEP-BY-STEP DEPLOYMENT

### 🖥️ STEP 1: VPS SETUP (Hetzner CX11)

#### 1.1 Create Hetzner Server
1. Go to [hetzner.com/cloud](https://www.hetzner.com/cloud)
2. Create account and project
3. **Server specs:**
   - **Type**: CX11 (2GB RAM, 1 vCPU, 20GB SSD)
   - **Location**: Falkenstein (Germany) or Helsinki (Finland)
   - **Image**: Ubuntu 22.04 LTS
   - **SSH Key**: Upload your public key
   - **Cost**: €4.15/month

#### 1.2 Initial Server Setup
```bash
# Connect to your server
ssh root@YOUR_SERVER_IP

# Download and run setup script
wget https://raw.githubusercontent.com/YOUR_USERNAME/SolanSuperagent/main/setup-vps.sh
chmod +x setup-vps.sh
./setup-vps.sh
```

#### 1.3 Upload Configuration
```bash
# From your local machine, upload .env file
scp .env root@YOUR_SERVER_IP:/opt/solan/.env

# Verify upload
ssh root@YOUR_SERVER_IP "cat /opt/solan/.env | head -5"
```

#### 1.4 Deploy Backend
```bash
# On your server
ssh root@YOUR_SERVER_IP
cd /opt/solan
./deploy-production.sh
```

### 🌐 STEP 2: VERCEL FRONTEND SETUP

#### 2.1 GitHub Repository
```bash
# Ensure your code is pushed to GitHub
git add .
git commit -m "Add Vercel frontend configuration"
git push origin main
```

#### 2.2 Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub account
3. Click "New Project"
4. Import your repository
5. **Configuration:**
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

#### 2.3 Environment Variables in Vercel
In Vercel dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_API_BASE=https://api.solanai.ai
NEXT_PUBLIC_SITE_URL=https://solanai.ai
```

#### 2.4 Custom Domain Setup
1. In Vercel dashboard → Settings → Domains
2. Add domains:
   - `solanai.ai`
   - `www.solanai.ai`
3. Follow DNS configuration instructions

### 🌍 STEP 3: DNS CONFIGURATION

Configure these DNS records with your domain provider:

```
Type    Name              Value                    TTL
A       solanai.ai        76.76.19.19             300  # Vercel IP (auto-provided)
A       www.solanai.ai    76.76.19.19             300  # Vercel IP (auto-provided)
A       api.solanai.ai    YOUR_HETZNER_SERVER_IP  300  # Your VPS IP
```

**Note**: Vercel will provide the exact IP addresses in their dashboard.

### 🧪 STEP 4: TESTING & VERIFICATION

#### 4.1 Backend Tests
```bash
# Test API health
curl -i https://api.solanai.ai/api/health
# Expected: {"status":"ok","version":"3.0"}

# Test bias detection
curl -i -X POST -H "Content-Type: application/json" \
  -d '{"text":"Women are always more emotional"}' \
  https://api.solanai.ai/api/analyzer/bias

# Run full verification
ssh root@YOUR_SERVER_IP "cd /opt/solan && ./verify-production.sh"
```

#### 4.2 Frontend Tests
```bash
# Test landing page
curl -I https://solanai.ai
# Expected: 200 OK

# Test invite API
curl -i -X POST -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","reason":"Testing the platform"}' \
  https://solanai.ai/api/invite
```

#### 4.3 Integration Tests
Open browser and test:
1. **Landing page**: `https://solanai.ai`
2. **Observatorium**: `https://solanai.ai/dashboard`
3. **API calls**: No CORS errors in browser console
4. **Invite form**: Submits successfully

## 🔒 SECURITY CHECKLIST

### ✅ Backend Security
- [ ] Health endpoint: `https://api.solanai.ai/api/health` responds
- [ ] Rate limiting: 429 after ~60 requests/minute
- [ ] PII redaction: Emails/phones masked in responses
- [ ] CORS: Only allows `https://solanai.ai` and `https://www.solanai.ai`
- [ ] Firewall: Only ports 22, 80, 443 open
- [ ] SSL: Let's Encrypt certificates active

### ✅ Frontend Security
- [ ] HTTPS: All traffic encrypted
- [ ] Security headers: CSP, X-Frame-Options, etc.
- [ ] API calls: Use HTTPS endpoints only
- [ ] Environment variables: No secrets in client code

## 💰 COST BREAKDOWN

### Monthly Costs:
- **Vercel**: €0 (Hobby plan, 100GB bandwidth)
- **Hetzner CX11**: €4.15/month
- **Domain**: ~€1/month (€12/year)
- **Total**: ~€5.15/month

### Scaling Options:
- **Vercel Pro**: €20/month (unlimited bandwidth, analytics)
- **Hetzner CX21**: €8.30/month (4GB RAM, better performance)
- **CDN**: Optional, included in Vercel Pro

## 🛠️ MANAGEMENT & MONITORING

### Daily Operations
```bash
# Check backend status
ssh root@YOUR_SERVER_IP "cd /opt/solan && docker-compose ps"

# View logs
ssh root@YOUR_SERVER_IP "cd /opt/solan && docker-compose logs -f --tail=50"

# Update backend
ssh root@YOUR_SERVER_IP "cd /opt/solan && git pull && docker-compose up -d --build"
```

### Monitoring Setup
1. **Uptime monitoring**: UptimeRobot or Pingdom
   - Monitor: `https://api.solanai.ai/api/health`
   - Interval: 1 minute
   
2. **Log monitoring**: 
   - Backend logs: `/opt/solan/logs/immutable_log.jsonl`
   - Vercel logs: Available in Vercel dashboard

3. **Performance monitoring**:
   - Vercel Analytics (built-in)
   - Server monitoring: `htop`, `docker stats`

## 🔄 DEPLOYMENT WORKFLOW

### Frontend Updates (Automatic)
1. Push to GitHub `main` branch
2. Vercel auto-deploys within 1-2 minutes
3. Preview deployments for feature branches

### Backend Updates (Manual)
```bash
# On your local machine
git push origin main

# On your server
ssh root@YOUR_SERVER_IP
cd /opt/solan
git pull
docker-compose -f docker-compose.production.yml up -d --build
```

### Rollback Procedures
```bash
# Frontend: Use Vercel dashboard to rollback
# Backend: 
ssh root@YOUR_SERVER_IP
cd /opt/solan
git checkout HEAD~1  # Go back one commit
docker-compose -f docker-compose.production.yml up -d --build
```

## 🆘 TROUBLESHOOTING

### Common Issues

1. **DNS not resolving**
   - Wait up to 24 hours for global propagation
   - Use `nslookup` to verify DNS records

2. **CORS errors**
   - Check `ALLOW_ORIGINS` in backend `.env`
   - Verify Vercel domain matches CORS settings

3. **SSL certificate issues**
   - Check Let's Encrypt logs: `docker logs letsencrypt`
   - Verify domain DNS points to correct IP

4. **API timeouts**
   - Check VPS firewall: `ufw status`
   - Verify Docker containers: `docker ps`

### Support Resources
- **Hetzner Support**: [docs.hetzner.com](https://docs.hetzner.com)
- **Vercel Support**: [vercel.com/docs](https://vercel.com/docs)
- **Docker Issues**: Check container logs with `docker logs [container_name]`

---

## 🎉 SUCCESS CRITERIA

Your deployment is successful when:

✅ **Frontend**: `https://solanai.ai` loads instantly  
✅ **Backend**: `https://api.solanai.ai/api/health` returns `{"status":"ok","version":"3.0"}`  
✅ **Integration**: No CORS errors in browser console  
✅ **Security**: Rate limiting and PII redaction working  
✅ **Performance**: Sub-200ms API responses  

**🚀 Congratulations! Your Solān v3.0 platform is now live with enterprise-grade security and global CDN performance!**
