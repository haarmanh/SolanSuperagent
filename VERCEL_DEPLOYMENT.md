# 🚀 Solān v3.0 - Vercel Deployment Guide

## 📋 QUICK DEPLOYMENT STEPS

### 1️⃣ Push to GitHub
```bash
# Add all frontend files
git add .
git commit -m "Add Solān v3.0 frontend for Vercel deployment"
git push origin main
```

### 2️⃣ Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click "New Project"
4. Import your repository
5. **Configuration:**
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3️⃣ Environment Variables
In Vercel dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_API_BASE=https://api.solanai.ai
NEXT_PUBLIC_SITE_URL=https://solanai.ai
```

### 4️⃣ Custom Domain
1. In Vercel dashboard → Settings → Domains
2. Add domains:
   - `solanai.ai`
   - `www.solanai.ai`
3. Follow DNS configuration instructions

## 🌐 DNS CONFIGURATION

Configure these DNS records with your domain provider:

```
Type    Name              Value                    TTL
A       solanai.ai        76.76.19.19             300  # Vercel IP (auto-provided)
A       www.solanai.ai    76.76.19.19             300  # Vercel IP (auto-provided)
A       api.solanai.ai    YOUR_VPS_SERVER_IP      300  # Your backend server
```

**Note**: Vercel will provide the exact IP addresses in their dashboard.

## 🧪 TESTING AFTER DEPLOYMENT

### Frontend Tests
```bash
# Test landing page
curl -I https://solanai.ai
# Expected: 200 OK

# Test dashboard
curl -I https://solanai.ai/dashboard
# Expected: 200 OK
```

### Integration Tests
Open browser and test:
1. **Landing page**: `https://solanai.ai`
2. **API status**: Green dot should show "API Online"
3. **Dashboard**: `https://solanai.ai/dashboard`
4. **Analysis**: Try bias detection, alignment, coherence
5. **Invite form**: Submit test invite

## 🔧 LOCAL DEVELOPMENT

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

## 📊 FEATURES INCLUDED

### ✅ Landing Page (`/`)
- Professional hero section
- Feature showcase
- API status indicator
- Invite form with validation
- Responsive design

### ✅ Dashboard (`/dashboard`)
- Real-time API health monitoring
- Bias detection interface
- Ethical alignment analysis
- Coherence analysis
- Audit trail viewer
- Quick test actions

### ✅ API Integration
- Connects to your backend at `api.solanai.ai`
- Real-time health checks
- All analysis endpoints
- Echo testing
- Log viewing

### ✅ Security & Performance
- HTTPS only
- Security headers
- CORS protection
- Rate limiting awareness
- Error handling

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. **Test all functionality**
2. **Set up monitoring** (Vercel Analytics)
3. **Configure alerts** (UptimeRobot)
4. **Add custom analytics** (optional)
5. **Set up staging environment** (optional)

## 🆘 TROUBLESHOOTING

### Common Issues

1. **Build fails**
   - Check Node.js version (18+)
   - Verify all dependencies installed
   - Check for TypeScript errors

2. **API calls fail**
   - Verify `NEXT_PUBLIC_API_BASE` environment variable
   - Check CORS settings on backend
   - Ensure backend is running

3. **Domain not working**
   - Wait for DNS propagation (up to 24 hours)
   - Verify DNS records are correct
   - Check Vercel domain configuration

### Support Resources
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **Tailwind CSS**: [tailwindcss.com/docs](https://tailwindcss.com/docs)

---

## 🎉 SUCCESS CRITERIA

Your deployment is successful when:

✅ **Frontend**: `https://solanai.ai` loads with professional design  
✅ **Dashboard**: `https://solanai.ai/dashboard` shows API status  
✅ **Integration**: Analysis tools work without CORS errors  
✅ **Performance**: Fast loading with Vercel CDN  
✅ **Mobile**: Responsive design works on all devices  

**🚀 Congratulations! Your Solān v3.0 platform is now live with professional frontend and enterprise backend!**
