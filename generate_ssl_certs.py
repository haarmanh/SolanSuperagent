#!/usr/bin/env python3
"""
Generate SSL certificates for local HTTPS development
"""

import os
import subprocess
import sys
from pathlib import Path

def generate_ssl_certificates():
    """Generate self-signed SSL certificates for local development"""
    
    print("🔒 Generating SSL certificates for local HTTPS development...")
    
    # Create certs directory
    certs_dir = Path("certs")
    certs_dir.mkdir(exist_ok=True)
    
    cert_file = certs_dir / "cert.pem"
    key_file = certs_dir / "key.pem"
    
    # Check if certificates already exist
    if cert_file.exists() and key_file.exists():
        print("✅ SSL certificates already exist")
        print(f"   Certificate: {cert_file}")
        print(f"   Private Key: {key_file}")
        return True
    
    # Generate self-signed certificate
    try:
        print("🔧 Generating self-signed certificate...")
        
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", str(key_file),
            "-out", str(cert_file),
            "-days", "365",
            "-nodes",
            "-subj", "/C=NL/ST=Netherlands/L=Amsterdam/O=Solan/OU=Development/CN=localhost"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SSL certificates generated successfully!")
            print(f"   Certificate: {cert_file}")
            print(f"   Private Key: {key_file}")
            print()
            print("⚠️  These are self-signed certificates for development only!")
            print("   Your browser will show a security warning - this is normal.")
            print("   For production, use certificates from a trusted CA.")
            return True
        else:
            print(f"❌ Error generating certificates: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ OpenSSL not found!")
        print("   Please install OpenSSL:")
        print("   - Windows: Download from https://slproweb.com/products/Win32OpenSSL.html")
        print("   - macOS: brew install openssl")
        print("   - Linux: sudo apt-get install openssl (Ubuntu/Debian)")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🌟 Solan SSL Certificate Generator")
    print("=" * 50)
    
    if generate_ssl_certificates():
        print()
        print("🚀 Ready for HTTPS!")
        print("   Run: python start_secure_web_interface.py")
        print("   Set USE_HTTPS=true in your .env file")
    else:
        print()
        print("❌ Certificate generation failed")
        print("   You can still run HTTP for local development")
        sys.exit(1)

if __name__ == "__main__":
    main()
