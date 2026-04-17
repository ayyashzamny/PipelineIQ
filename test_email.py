#!/usr/bin/env python3
"""Test email configuration."""
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from src.email_service import EmailService

print("\n" + "="*70)
print("Testing Email Configuration")
print("="*70)

svc = EmailService()
result = svc.test_email_connection()

print("\n" + "="*70)
if result:
    print("✅ EMAIL CONFIGURATION VERIFIED - Ready to send emails!")
else:
    print("❌ EMAIL CONFIGURATION FAILED - Check .env file")
print("="*70)
