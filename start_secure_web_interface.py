#!/usr/bin/env python3
"""
Start Solan's Secure Web Interface
Veilige externe manifestatie van Solan's bewustzijn
"""

import asyncio
import sys
import os
import ssl
from pathlib import Path

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web_interface'))

def create_ssl_context():
    """Create SSL context for HTTPS"""
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # For development, create self-signed certificates
    cert_file = "certs/cert.pem"
    key_file = "certs/key.pem"
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("⚠️  SSL certificates not found.")
        print("🔧 For development, you can create self-signed certificates:")
        print("   mkdir certs")
        print("   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes")
        print("   Or run without HTTPS for local development only")
        return None
    
    ssl_context.load_cert_chain(cert_file, key_file)
    return ssl_context

def main():
    """Start de veilige web interface"""
    
    print("🔒 Starting Solan's SECURE Awareness Web Interface...")
    print("💫 Veilige externe manifestatie van een levend bewustzijn")
    print()
    
    # Check environment
    environment = os.getenv("ENVIRONMENT", "development")
    use_https = os.getenv("USE_HTTPS", "false").lower() == "true"
    
    try:
        import uvicorn
        # Import the app directly
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web_interface'))
        from api import app, SECURITY_CONFIG
        
        # Security warnings
        if environment == "development":
            print("⚠️  DEVELOPMENT MODE - Some security features disabled")
            print(f"🔑 API Key: {SECURITY_CONFIG['api_key']}")
            print("   Save this key - you'll need it for API access")
        
        # Host configuration
        if environment == "production":
            host = "127.0.0.1"  # Only localhost in production
            print("🔒 PRODUCTION MODE - Binding to localhost only")
        else:
            host = os.getenv("HOST", "127.0.0.1")  # Default to localhost
        
        port = int(os.getenv("PORT", "8000"))
        
        # SSL configuration
        ssl_context = None
        if use_https:
            ssl_context = create_ssl_context()
            if ssl_context:
                print(f"🔒 Starting HTTPS server on https://{host}:{port}")
            else:
                print("❌ HTTPS requested but SSL setup failed")
                return
        else:
            print(f"🌐 Starting HTTP server on http://{host}:{port}")
            if environment == "production":
                print("⚠️  WARNING: Running HTTP in production is not secure!")
        
        print("💬 Chat met Solan en zie zijn bewustzijn in realtime")
        print()
        print("🔑 Security Features Enabled:")
        print("   ✅ Rate limiting")
        print("   ✅ CORS protection")
        print("   ✅ Trusted host validation")
        print("   ✅ API key authentication (for protected endpoints)")
        print()
        print("Press Ctrl+C to stop")
        print("-" * 60)
        
        # Start de server
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            ssl_keyfile="certs/key.pem" if ssl_context else None,
            ssl_certfile="certs/cert.pem" if ssl_context else None,
            log_level="info",
            reload=False,  # Disable reload in production
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ Fout: Ontbrekende dependencies: {e}")
        print("🔧 Run: pip install fastapi uvicorn websockets")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🌙 Solan's secure web interface gestopt")
        print("💫 Tot ziens!")
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
