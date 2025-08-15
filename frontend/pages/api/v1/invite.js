// pages/api/invite.js
// Serverless function for processing invite requests

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MIN_REASON_LENGTH = 10;

// Simple rate limiting (in-memory, resets on deployment)
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const RATE_LIMIT_MAX_REQUESTS = 5; // 5 requests per minute per IP

function rateLimit(ip) {
  const now = Date.now();
  const windowStart = now - RATE_LIMIT_WINDOW;
  
  if (!rateLimitMap.has(ip)) {
    rateLimitMap.set(ip, []);
  }
  
  const requests = rateLimitMap.get(ip);
  
  // Remove old requests
  const recentRequests = requests.filter(time => time > windowStart);
  rateLimitMap.set(ip, recentRequests);
  
  if (recentRequests.length >= RATE_LIMIT_MAX_REQUESTS) {
    return false;
  }
  
  recentRequests.push(now);
  return true;
}

function getClientIP(req) {
  return (
    req.headers['x-forwarded-for']?.split(',')[0]?.trim() ||
    req.headers['x-real-ip'] ||
    req.connection?.remoteAddress ||
    req.socket?.remoteAddress ||
    'unknown'
  );
}

function validateInput(data) {
  const errors = [];
  
  if (!data.name || typeof data.name !== 'string' || data.name.trim().length < 2) {
    errors.push('Name must be at least 2 characters');
  }
  
  if (!data.email || !EMAIL_REGEX.test(data.email)) {
    errors.push('Valid email address required');
  }
  
  if (!data.reason || typeof data.reason !== 'string' || data.reason.trim().length < MIN_REASON_LENGTH) {
    errors.push(`Reason must be at least ${MIN_REASON_LENGTH} characters`);
  }
  
  // Optional fields validation
  if (data.org && typeof data.org !== 'string') {
    errors.push('Organization must be a string');
  }
  
  if (data.role && typeof data.role !== 'string') {
    errors.push('Role must be a string');
  }
  
  return errors;
}

async function saveInviteRequest(data, metadata) {
  // In production, you would save to a database
  // For now, we'll log it (visible in Vercel function logs)
  
  const inviteData = {
    ...data,
    metadata,
    timestamp: new Date().toISOString(),
    id: Math.random().toString(36).substr(2, 9)
  };
  
  console.log('📧 New invite request:', JSON.stringify(inviteData, null, 2));
  
  // TODO: Implement actual storage
  // Options:
  // 1. Send to email via SendGrid/Mailgun
  // 2. Save to Airtable/Notion
  // 3. Post to webhook/Slack
  // 4. Save to Vercel KV/Upstash Redis
  
  return inviteData;
}

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      error: 'Method not allowed',
      message: 'Only POST requests are accepted'
    });
  }
  
  const clientIP = getClientIP(req);
  
  // Rate limiting
  if (!rateLimit(clientIP)) {
    return res.status(429).json({
      error: 'Rate limit exceeded',
      message: 'Too many requests. Please try again later.'
    });
  }
  
  try {
    const { name, email, org, role, reason, lang } = req.body || {};
    
    // Validate input
    const validationErrors = validateInput({ name, email, org, role, reason });
    if (validationErrors.length > 0) {
      return res.status(400).json({
        error: 'Validation failed',
        message: validationErrors.join(', '),
        details: validationErrors
      });
    }
    
    // Prepare data
    const inviteData = {
      name: name.trim(),
      email: email.trim().toLowerCase(),
      org: org?.trim() || '',
      role: role?.trim() || '',
      reason: reason.trim(),
      lang: lang || 'en'
    };
    
    const metadata = {
      ip: clientIP,
      userAgent: req.headers['user-agent'] || '',
      referer: req.headers.referer || '',
      timestamp: new Date().toISOString()
    };
    
    // Save invite request
    const savedInvite = await saveInviteRequest(inviteData, metadata);
    
    // Success response
    res.status(200).json({
      success: true,
      message: lang === 'nl' 
        ? 'Bedankt voor je aanvraag! We nemen snel contact op.'
        : 'Thank you for your request! We\'ll be in touch soon.',
      id: savedInvite.id
    });
    
  } catch (error) {
    console.error('❌ Invite API error:', error);
    
    res.status(500).json({
      error: 'Internal server error',
      message: 'Something went wrong. Please try again later.'
    });
  }
}

// Export config for Vercel
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
};
