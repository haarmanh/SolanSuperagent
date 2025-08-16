#!/usr/bin/env node

/**
 * 🛡️ SOLAN SECURITY DASHBOARD
 * Real-time security monitoring and threat detection
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 🎨 Console colors
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    white: '\x1b[37m'
};

// 🛡️ Security configuration
const config = {
    endpoints: {
        vercel: 'https://private.solanai.ai',
        hetzner: 'http://95.216.209.234:8000',
        health: '/health'
    },
    security: {
        maxResponseTime: 5000,
        minSecurityScore: 80,
        threatThreshold: 3
    },
    monitoring: {
        interval: 30000, // 30 seconds
        alertCooldown: 300000 // 5 minutes
    }
};

class SecurityDashboard {
    constructor() {
        this.alerts = [];
        this.metrics = {
            uptime: 0,
            responseTime: 0,
            securityScore: 0,
            threatLevel: 'LOW',
            lastCheck: null
        };
        this.lastAlert = 0;
    }

    // 🎨 Display methods
    log(message, color = 'white') {
        const timestamp = new Date().toISOString();
        console.log(`${colors[color]}[${timestamp}] ${message}${colors.reset}`);
    }

    success(message) {
        this.log(`✅ ${message}`, 'green');
    }

    warning(message) {
        this.log(`⚠️ ${message}`, 'yellow');
    }

    error(message) {
        this.log(`❌ ${message}`, 'red');
    }

    info(message) {
        this.log(`ℹ️ ${message}`, 'blue');
    }

    // 🔍 Security checks
    async checkEndpoint(url, name) {
        return new Promise((resolve) => {
            const startTime = Date.now();
            const client = url.startsWith('https') ? https : http;
            
            const req = client.get(url, (res) => {
                const responseTime = Date.now() - startTime;
                const statusCode = res.statusCode;
                
                // Check security headers
                const securityHeaders = {
                    'x-frame-options': res.headers['x-frame-options'],
                    'x-content-type-options': res.headers['x-content-type-options'],
                    'strict-transport-security': res.headers['strict-transport-security'],
                    'content-security-policy': res.headers['content-security-policy']
                };
                
                const securityScore = this.calculateSecurityScore(securityHeaders);
                
                resolve({
                    name,
                    url,
                    statusCode,
                    responseTime,
                    securityScore,
                    securityHeaders,
                    healthy: statusCode === 200 && responseTime < config.security.maxResponseTime
                });
            });
            
            req.on('error', (error) => {
                resolve({
                    name,
                    url,
                    statusCode: 0,
                    responseTime: Date.now() - startTime,
                    securityScore: 0,
                    error: error.message,
                    healthy: false
                });
            });
            
            req.setTimeout(config.security.maxResponseTime, () => {
                req.destroy();
                resolve({
                    name,
                    url,
                    statusCode: 0,
                    responseTime: config.security.maxResponseTime,
                    securityScore: 0,
                    error: 'Timeout',
                    healthy: false
                });
            });
        });
    }

    calculateSecurityScore(headers) {
        let score = 0;
        const maxScore = 100;
        
        // Check for security headers (25 points each)
        if (headers['x-frame-options']) score += 25;
        if (headers['x-content-type-options']) score += 25;
        if (headers['strict-transport-security']) score += 25;
        if (headers['content-security-policy']) score += 25;
        
        return Math.min(score, maxScore);
    }

    async performSecurityScan() {
        this.info('🔍 Starting security scan...');
        
        const checks = [
            this.checkEndpoint(config.endpoints.vercel, 'Vercel'),
            this.checkEndpoint(config.endpoints.hetzner + config.endpoints.health, 'Hetzner API')
        ];
        
        const results = await Promise.all(checks);
        
        // Update metrics
        this.metrics.lastCheck = new Date();
        this.metrics.responseTime = Math.max(...results.map(r => r.responseTime));
        this.metrics.securityScore = Math.min(...results.map(r => r.securityScore));
        this.metrics.uptime = results.every(r => r.healthy) ? 100 : 0;
        
        // Determine threat level
        const unhealthyCount = results.filter(r => !r.healthy).length;
        const lowSecurityCount = results.filter(r => r.securityScore < config.security.minSecurityScore).length;
        
        if (unhealthyCount > 0 || lowSecurityCount > 0) {
            this.metrics.threatLevel = unhealthyCount > 1 ? 'HIGH' : 'MEDIUM';
        } else {
            this.metrics.threatLevel = 'LOW';
        }
        
        return results;
    }

    displayDashboard(results) {
        // Clear screen
        console.clear();
        
        // Header
        console.log(`${colors.cyan}${colors.bright}`);
        console.log('🛡️ ═══════════════════════════════════════════════════════════════');
        console.log('   SOLAN SECURITY FORTRESS - REAL-TIME MONITORING DASHBOARD');
        console.log('═══════════════════════════════════════════════════════════════');
        console.log(`${colors.reset}`);
        
        // System status
        const statusColor = this.metrics.uptime === 100 ? 'green' : 'red';
        console.log(`${colors[statusColor]}🚀 SYSTEM STATUS: ${this.metrics.uptime === 100 ? 'OPERATIONAL' : 'DEGRADED'}${colors.reset}`);
        console.log(`${colors.blue}⏰ Last Check: ${this.metrics.lastCheck?.toLocaleString()}${colors.reset}`);
        console.log('');
        
        // Threat level
        const threatColor = this.metrics.threatLevel === 'LOW' ? 'green' : 
                           this.metrics.threatLevel === 'MEDIUM' ? 'yellow' : 'red';
        console.log(`${colors[threatColor]}🚨 THREAT LEVEL: ${this.metrics.threatLevel}${colors.reset}`);
        console.log('');
        
        // Metrics
        console.log(`${colors.cyan}📊 SECURITY METRICS:${colors.reset}`);
        console.log(`   🛡️ Security Score: ${this.metrics.securityScore}%`);
        console.log(`   ⚡ Response Time: ${this.metrics.responseTime}ms`);
        console.log(`   🔄 Uptime: ${this.metrics.uptime}%`);
        console.log('');
        
        // Endpoint details
        console.log(`${colors.cyan}🌐 ENDPOINT STATUS:${colors.reset}`);
        results.forEach(result => {
            const statusIcon = result.healthy ? '✅' : '❌';
            const statusColor = result.healthy ? 'green' : 'red';
            
            console.log(`${colors[statusColor]}${statusIcon} ${result.name}${colors.reset}`);
            console.log(`   📍 URL: ${result.url}`);
            console.log(`   📊 Status: ${result.statusCode} (${result.responseTime}ms)`);
            console.log(`   🛡️ Security: ${result.securityScore}%`);
            
            if (result.error) {
                console.log(`   ❌ Error: ${result.error}`);
            }
            
            console.log('');
        });
        
        // Recent alerts
        if (this.alerts.length > 0) {
            console.log(`${colors.yellow}🚨 RECENT ALERTS:${colors.reset}`);
            this.alerts.slice(-5).forEach(alert => {
                console.log(`   ${alert.timestamp}: ${alert.message}`);
            });
            console.log('');
        }
        
        // Footer
        console.log(`${colors.cyan}═══════════════════════════════════════════════════════════════${colors.reset}`);
        console.log(`${colors.blue}🔄 Auto-refresh every ${config.monitoring.interval / 1000}s | Press Ctrl+C to exit${colors.reset}`);
    }

    addAlert(message, level = 'warning') {
        const alert = {
            timestamp: new Date().toLocaleString(),
            message,
            level
        };
        
        this.alerts.push(alert);
        
        // Keep only last 10 alerts
        if (this.alerts.length > 10) {
            this.alerts = this.alerts.slice(-10);
        }
        
        // Rate limit alerts
        const now = Date.now();
        if (now - this.lastAlert > config.monitoring.alertCooldown) {
            if (level === 'error') {
                this.error(message);
            } else {
                this.warning(message);
            }
            this.lastAlert = now;
        }
    }

    async start() {
        this.info('🛡️ Starting Solan Security Dashboard...');
        this.info('🔍 Initializing security monitoring...');
        
        const monitor = async () => {
            try {
                const results = await this.performSecurityScan();
                
                // Check for issues
                results.forEach(result => {
                    if (!result.healthy) {
                        this.addAlert(`${result.name} is unhealthy: ${result.error || 'Unknown error'}`, 'error');
                    }
                    
                    if (result.securityScore < config.security.minSecurityScore) {
                        this.addAlert(`${result.name} has low security score: ${result.securityScore}%`, 'warning');
                    }
                    
                    if (result.responseTime > config.security.maxResponseTime) {
                        this.addAlert(`${result.name} has slow response: ${result.responseTime}ms`, 'warning');
                    }
                });
                
                this.displayDashboard(results);
                
            } catch (error) {
                this.error(`Security scan failed: ${error.message}`);
            }
        };
        
        // Initial scan
        await monitor();
        
        // Set up monitoring interval
        setInterval(monitor, config.monitoring.interval);
        
        // Handle graceful shutdown
        process.on('SIGINT', () => {
            this.info('🛡️ Security dashboard shutting down...');
            process.exit(0);
        });
    }
}

// 🚀 Start the dashboard
if (require.main === module) {
    const dashboard = new SecurityDashboard();
    dashboard.start().catch(error => {
        console.error('Failed to start security dashboard:', error);
        process.exit(1);
    });
}

module.exports = SecurityDashboard;
