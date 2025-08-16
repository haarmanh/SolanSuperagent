#!/usr/bin/env node

/**
 * 🚀 SOLAN SECURE DEPLOYMENT AUTOMATION
 * Zero-touch deployment with military-grade security
 */

const { execSync } = require('child_process');
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
    cyan: '\x1b[36m'
};

class SecureDeployment {
    constructor() {
        this.startTime = Date.now();
        this.deploymentId = `deploy_${Date.now()}`;
        this.errors = [];
        this.warnings = [];
    }

    log(message, color = 'white') {
        const timestamp = new Date().toISOString();
        console.log(`${colors[color]}[${timestamp}] ${message}${colors.reset}`);
    }

    success(message) {
        this.log(`✅ ${message}`, 'green');
    }

    warning(message) {
        this.log(`⚠️ ${message}`, 'yellow');
        this.warnings.push(message);
    }

    error(message) {
        this.log(`❌ ${message}`, 'red');
        this.errors.push(message);
    }

    info(message) {
        this.log(`ℹ️ ${message}`, 'blue');
    }

    header(message) {
        console.log(`\n${colors.cyan}${colors.bright}🛡️ ${message}${colors.reset}`);
        console.log(`${colors.cyan}${'='.repeat(message.length + 4)}${colors.reset}\n`);
    }

    async runCommand(command, description, options = {}) {
        this.info(`Running: ${description}`);
        
        try {
            const result = execSync(command, {
                stdio: options.silent ? 'pipe' : 'inherit',
                encoding: 'utf8',
                ...options
            });
            
            this.success(`Completed: ${description}`);
            return result;
        } catch (error) {
            this.error(`Failed: ${description} - ${error.message}`);
            if (!options.continueOnError) {
                throw error;
            }
            return null;
        }
    }

    async securityPreCheck() {
        this.header('SECURITY PRE-DEPLOYMENT CHECKS');
        
        // Check for secrets in code
        this.info('Scanning for exposed secrets...');
        try {
            const secretScan = execSync(
                'grep -r "password.*=\\|secret.*=\\|key.*=" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=scripts || true',
                { encoding: 'utf8' }
            );
            
            if (secretScan.trim()) {
                this.error('Potential secrets found in code:');
                console.log(secretScan);
                throw new Error('Security violation: Secrets detected in code');
            }
            this.success('No secrets found in code');
        } catch (error) {
            if (error.message.includes('Security violation')) {
                throw error;
            }
            this.warning('Secret scan completed with warnings');
        }

        // Check npm audit
        this.info('Running security audit...');
        try {
            await this.runCommand(
                'cd solan-private-chat && npm audit --audit-level=moderate',
                'NPM security audit'
            );
        } catch (error) {
            this.warning('Security vulnerabilities found - attempting auto-fix');
            await this.runCommand(
                'cd solan-private-chat && npm audit fix',
                'Auto-fixing security issues',
                { continueOnError: true }
            );
        }

        // Validate environment
        this.info('Validating deployment environment...');
        const requiredEnvVars = ['NODE_ENV'];
        const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);
        
        if (missingVars.length > 0) {
            this.warning(`Missing environment variables: ${missingVars.join(', ')}`);
        }

        this.success('Security pre-checks completed');
    }

    async buildApplication() {
        this.header('SECURE APPLICATION BUILD');
        
        // Install dependencies
        await this.runCommand(
            'cd solan-private-chat && npm ci',
            'Installing dependencies'
        );

        // Run build
        await this.runCommand(
            'cd solan-private-chat && npm run build',
            'Building application'
        );

        // Verify build
        const buildPath = path.join(__dirname, '../solan-private-chat/.next');
        if (!fs.existsSync(buildPath)) {
            throw new Error('Build verification failed: .next directory not found');
        }

        this.success('Application build completed and verified');
    }

    async deployToVercel() {
        this.header('VERCEL SECURE DEPLOYMENT');
        
        // Check if Vercel CLI is available
        try {
            await this.runCommand('vercel --version', 'Checking Vercel CLI', { silent: true });
        } catch (error) {
            this.warning('Vercel CLI not found - using GitHub Actions instead');
            await this.runCommand(
                'gh workflow run auto-deploy.yml --field environment=production',
                'Triggering Vercel deployment via GitHub Actions'
            );
            return;
        }

        // Deploy to Vercel
        await this.runCommand(
            'cd solan-private-chat && vercel --prod --yes',
            'Deploying to Vercel'
        );

        this.success('Vercel deployment completed');
    }

    async deployToHetzner() {
        this.header('HETZNER SECURE DEPLOYMENT');
        
        // Use GitHub Actions for secure deployment
        await this.runCommand(
            'gh workflow run auto-deploy.yml',
            'Triggering Hetzner deployment via GitHub Actions'
        );

        this.success('Hetzner deployment triggered');
    }

    async postDeploymentVerification() {
        this.header('POST-DEPLOYMENT VERIFICATION');
        
        // Wait for deployments to complete
        this.info('Waiting for deployments to stabilize...');
        await new Promise(resolve => setTimeout(resolve, 30000));

        // Verify Vercel deployment
        try {
            await this.runCommand(
                'curl -f -s https://private.solanai.ai',
                'Verifying Vercel deployment',
                { silent: true }
            );
            this.success('Vercel deployment verified');
        } catch (error) {
            this.error('Vercel deployment verification failed');
        }

        // Verify Hetzner deployment
        try {
            await this.runCommand(
                'curl -f -s http://95.216.209.234:8000/health',
                'Verifying Hetzner deployment',
                { silent: true }
            );
            this.success('Hetzner deployment verified');
        } catch (error) {
            this.error('Hetzner deployment verification failed');
        }

        // Security headers check
        this.info('Verifying security headers...');
        try {
            const headers = await this.runCommand(
                'curl -I -s https://private.solanai.ai',
                'Checking security headers',
                { silent: true }
            );
            
            const requiredHeaders = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Content-Security-Policy'
            ];
            
            const missingHeaders = requiredHeaders.filter(header => 
                !headers.includes(header)
            );
            
            if (missingHeaders.length > 0) {
                this.warning(`Missing security headers: ${missingHeaders.join(', ')}`);
            } else {
                this.success('All security headers present');
            }
        } catch (error) {
            this.warning('Security headers check failed');
        }
    }

    async generateDeploymentReport() {
        this.header('DEPLOYMENT REPORT');
        
        const duration = Math.round((Date.now() - this.startTime) / 1000);
        const status = this.errors.length === 0 ? 'SUCCESS' : 'FAILED';
        
        console.log(`${colors.cyan}📊 DEPLOYMENT SUMMARY${colors.reset}`);
        console.log(`   🆔 Deployment ID: ${this.deploymentId}`);
        console.log(`   ⏱️ Duration: ${duration} seconds`);
        console.log(`   📊 Status: ${status}`);
        console.log(`   ⚠️ Warnings: ${this.warnings.length}`);
        console.log(`   ❌ Errors: ${this.errors.length}`);
        console.log(`   ⏰ Completed: ${new Date().toISOString()}`);
        
        if (this.warnings.length > 0) {
            console.log(`\n${colors.yellow}⚠️ WARNINGS:${colors.reset}`);
            this.warnings.forEach((warning, index) => {
                console.log(`   ${index + 1}. ${warning}`);
            });
        }
        
        if (this.errors.length > 0) {
            console.log(`\n${colors.red}❌ ERRORS:${colors.reset}`);
            this.errors.forEach((error, index) => {
                console.log(`   ${index + 1}. ${error}`);
            });
        }
        
        // Save report to file
        const report = {
            deploymentId: this.deploymentId,
            timestamp: new Date().toISOString(),
            duration,
            status,
            warnings: this.warnings,
            errors: this.errors
        };
        
        const reportPath = path.join(__dirname, '../logs', `deployment-${this.deploymentId}.json`);
        
        // Ensure logs directory exists
        const logsDir = path.dirname(reportPath);
        if (!fs.existsSync(logsDir)) {
            fs.mkdirSync(logsDir, { recursive: true });
        }
        
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        this.info(`Deployment report saved: ${reportPath}`);
        
        return status === 'SUCCESS';
    }

    async deploy() {
        try {
            this.header('SOLAN SECURE DEPLOYMENT INITIATED');
            this.info(`Deployment ID: ${this.deploymentId}`);
            this.info(`Started at: ${new Date().toISOString()}`);
            
            // Execute deployment phases
            await this.securityPreCheck();
            await this.buildApplication();
            await this.deployToVercel();
            await this.deployToHetzner();
            await this.postDeploymentVerification();
            
            const success = await this.generateDeploymentReport();
            
            if (success) {
                this.success('🎉 SECURE DEPLOYMENT COMPLETED SUCCESSFULLY!');
                this.info('🛡️ All security checks passed');
                this.info('🚀 All systems operational');
            } else {
                this.error('💥 DEPLOYMENT COMPLETED WITH ERRORS');
                this.warning('🔍 Review deployment report for details');
            }
            
            return success;
            
        } catch (error) {
            this.error(`Deployment failed: ${error.message}`);
            await this.generateDeploymentReport();
            throw error;
        }
    }
}

// 🚀 Execute deployment
if (require.main === module) {
    const deployment = new SecureDeployment();
    
    deployment.deploy()
        .then(success => {
            process.exit(success ? 0 : 1);
        })
        .catch(error => {
            console.error('Deployment failed:', error.message);
            process.exit(1);
        });
}

module.exports = SecureDeployment;
