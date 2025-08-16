# 🚀 GitHub + Vercel + VPS Setup Guide

## 📋 ARCHITECTURE OVERVIEW

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Users         │
│   (Vercel)      │    │   (VPS)         │    │                 │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ solanai.ai      │◄──►│ api.solanai.ai  │◄──►│ Browser/Apps    │
│ Landing Page    │    │ Solān API       │    │                 │
│ Observatorium   │    │ Secure Proxy    │    │                 │
│ /api/invite     │    │ Docker Stack    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 STEP 1: GITHUB REPOSITORY SETUP

### 1.1 Create Frontend Structure
```bash
mkdir frontend
cd frontend
npm init -y
npm install next react react-dom
```

### 1.2 Frontend Files Structure
```
frontend/
├── pages/
│   ├── index.js              # Landing page
│   ├── observatorium.js      # Analysis interface
│   └── api/
│       └── invite.js         # Invite processing
├── components/
│   ├── Layout.js
│   └── AnalysisInterface.js
├── public/
│   └── favicon.ico
├── package.json
├── next.config.js
└── vercel.json
```

### 1.3 Push to GitHub
```bash
# In your project root
git add .
git commit -m "Add Vercel frontend structure"
git push origin main
```

## 🌐 STEP 2: VERCEL DEPLOYMENT

### 2.1 Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Import your repository
4. Set build settings:
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`

### 2.2 Environment Variables in Vercel
```
NEXT_PUBLIC_API_BASE=https://api.solanai.ai
NEXT_PUBLIC_SITE_URL=https://solanai.ai
```

### 2.3 Custom Domain
1. In Vercel dashboard → Settings → Domains
2. Add: `solanai.ai` and `www.solanai.ai`
3. Configure DNS as instructed

## 🖥️ STEP 3: VPS SERVER SETUP

### 3.1 Choose VPS Provider
**Recommended options:**
- **Hetzner Cloud**: €4/month (2GB RAM, 40GB SSD)
- **DigitalOcean**: $6/month (1GB RAM, 25GB SSD)
- **Linode**: $5/month (1GB RAM, 25GB SSD)

### 3.2 Server Setup
```bash
# Connect to your server
ssh root@YOUR_SERVER_IP

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Create application directory
mkdir -p /opt/solan
cd /opt/solan

# Clone repository
git clone https://github.com/YOUR_USERNAME/SolanSuperagent.git .

# Upload .env file (from your local machine)
# scp .env root@YOUR_SERVER_IP:/opt/solan/.env
```

### 3.3 Deploy Backend
```bash
# On your server
chmod +x deploy-production.sh
./deploy-production.sh
```

## 🌍 STEP 4: DNS CONFIGURATION

### 4.1 DNS Records
Configure these DNS records with your domain provider:

```
Type    Name              Value                TTL
A       solanai.ai        76.76.19.19         300  # Vercel IP (example)
A       www.solanai.ai    76.76.19.19         300  # Vercel IP (example)
A       api.solanai.ai    YOUR_SERVER_IP      300  # Your VPS IP
```

### 4.2 Verify DNS
```bash
# Check frontend
nslookup solanai.ai
# Should point to Vercel

# Check backend
nslookup api.solanai.ai
# Should point to your server
```

## 🧪 STEP 5: TESTING & VERIFICATION

### 5.1 Frontend Tests
```bash
# Test landing page
curl -I https://solanai.ai
# Expected: 200 OK

# Test observatorium
curl -I https://solanai.ai/observatorium
# Expected: 200 OK
```

### 5.2 Backend Tests
```bash
# Test API health
curl -i https://api.solanai.ai/api/health
# Expected: {"status":"ok","version":"3.0"}

# Run full verification
./verify-production.sh
```

### 5.3 Integration Test
```bash
# Test frontend → backend communication
# In browser console on solanai.ai:
fetch('https://api.solanai.ai/api/health')
  .then(r => r.json())
  .then(console.log)
# Should work without CORS errors
```

## 🔧 STEP 6: CONTINUOUS DEPLOYMENT

### 6.1 GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Backend
on:
  push:
    branches: [main]
    paths: ['backend/**', 'docker-compose.production.yml']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /opt/solan
            git pull
            docker-compose -f docker-compose.production.yml up -d --build
```

### 6.2 Vercel Auto-Deploy
- ✅ Automatic on every push to `main`
- ✅ Preview deployments for PRs
- ✅ Rollback capability

## 💰 COST BREAKDOWN

### Monthly Costs:
- **Vercel**: €0 (Hobby plan, 100GB bandwidth)
- **VPS**: €4-6 (Hetzner/DigitalOcean)
- **Domain**: €1/month (€12/year)
- **Total**: ~€5-7/month

### Scaling Costs:
- **Vercel Pro**: €20/month (unlimited bandwidth)
- **Larger VPS**: €10-20/month (4GB+ RAM)
- **CDN**: Optional, €5-10/month

## 🚀 BENEFITS OF THIS SETUP

### ✅ Advantages:
- **Fast frontend**: Vercel CDN worldwide
- **Full backend control**: Docker, logs, custom logic
- **Cost effective**: ~€5/month total
- **Scalable**: Frontend auto-scales, backend upgradeable
- **Professional**: Custom domains, SSL, monitoring

### ⚠️ Considerations:
- **Two deployments**: Frontend (auto) + Backend (manual/CI)
- **Server maintenance**: OS updates, monitoring
- **Backup responsibility**: Your VPS data

## 🆘 TROUBLESHOOTING

### Common Issues:
1. **CORS errors**: Check `ALLOW_ORIGINS` in backend `.env`
2. **DNS propagation**: Wait 24h for global propagation
3. **SSL issues**: Verify both Vercel and Let's Encrypt certs
4. **API timeouts**: Check VPS firewall and Docker status

### Support Resources:
- **Vercel Docs**: https://vercel.com/docs
- **Docker Docs**: https://docs.docker.com
- **Your VPS provider support**

---

🎉 **Result: Professional AI Ethics Platform with Global CDN + Secure Backend!**
