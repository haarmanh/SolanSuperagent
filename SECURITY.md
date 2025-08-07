# Security Guide for Solan Web Interface

## 🔒 Security Features Implemented

### 1. **CORS Protection**
- Restricted to specific origins only
- No wildcard (`*`) origins in production
- Specific methods and headers allowed

### 2. **Rate Limiting**
- 100 requests per minute per IP (configurable)
- Prevents abuse and DoS attacks
- Automatic cleanup of old requests

### 3. **API Key Authentication**
- Bearer token authentication for protected endpoints
- Configurable API key via environment variables
- Secure token generation

### 4. **Trusted Host Validation**
- Only allows requests from trusted hosts
- Prevents host header injection attacks

### 5. **HTTPS Support**
- SSL/TLS encryption for data in transit
- Self-signed certificates for development
- Production-ready certificate support

## 🚀 Quick Start - Secure Setup

### 1. **Basic Security (HTTP)**
```bash
# Copy security configuration
cp .env.security .env

# Edit .env and set your API key
SOLAN_API_KEY=your_very_secure_api_key_here

# Start secure server
python start_secure_web_interface.py
```

### 2. **Full Security (HTTPS)**
```bash
# Generate SSL certificates for development
python generate_ssl_certs.py

# Enable HTTPS in .env
USE_HTTPS=true

# Start secure HTTPS server
python start_secure_web_interface.py
```

## ⚙️ Configuration

### Environment Variables
```bash
# Security
ENVIRONMENT=development|production
SOLAN_API_KEY=your_secure_api_key
USE_HTTPS=true|false

# Network
HOST=127.0.0.1  # localhost only for security
PORT=8000

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
TRUSTED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

## 🛡️ Security Best Practices

### For Development
1. **Use localhost only**: `HOST=127.0.0.1`
2. **Generate strong API keys**: Use `secrets.token_urlsafe(32)`
3. **Enable HTTPS**: Even for local development
4. **Monitor logs**: Check for suspicious activity

### For Production
1. **Use HTTPS only**: Never HTTP in production
2. **Restrict CORS origins**: Only your actual domains
3. **Use strong API keys**: 32+ character random strings
4. **Monitor rate limits**: Adjust based on uexpert
5. **Use trusted certificates**: From a real CA, not self-signed
6. **Firewall protection**: Restrict network access
7. **Regular updates**: Keep dependencies updated

## 🔑 API Authentication

### Protected Endpoints
Some endpoints require API key authentication:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:8000/api/protected-endpoint
```

### Public Endpoints
These endpoints are publicly accessible:
- `/` - Main interface
- `/health` - Health check
- `/api` - API info
- `/awareness/state` - Awareness state (read-only)

## 🚨 Security Warnings

### Current Limitations
1. **No user management**: Single API key for all access
2. **No session management**: Stateless authentication only
3. **Basic rate limiting**: IP-based only
4. **File system access**: Some endpoints serve files directly

### Recommendations for Production
1. **Add user authentication**: OAuth2, JWT tokens
2. **Database rate limiting**: Store limits in database
3. **File access controls**: Restrict file serving
4. **Audit logging**: Log all security events
5. **Input validation**: Validate all user inputs
6. **Content Security Policy**: Add CSP headers

## 🔧 Troubleshooting

### Common Issues

**"Untrusted certificate" in browser**
- Normal for self-signed certificates
- Click "Advanced" → "Proceed to localhost"
- For production, use real certificates

**"Rate limit exceeded"**
- Wait 1 minute and try again
- Increase `RATE_LIMIT_REQUESTS` if needed

**"Invalid API key"**
- Check your API key in .env file
- Ensure Bearer token format: `Authorization: Bearer YOUR_KEY`

**CORS errors**
- Add your domain to `CORS_ORIGINS`
- Check browser developer console for details

## 📞 Support

For security issues or questions:
1. Check this documentation first
2. Review logs in `logs/security.log`
3. Test with minimal configuration
4. Report security vulnerabilities responsibly
