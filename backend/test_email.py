#!/usr/bin/env python3
"""
Test script to diagnose email sending issues
"""

import os
import sys

# Add the project to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yolo_project.settings')

import django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test email sending functionality"""
    print("Testing email sending...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    
    try:
        # Test connection first
        import smtplib
        from email.mime.text import MIMEText
        
        # Create SMTP connection
        print("\nConnecting to SMTP server...")
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        print("TLS connection established.")
        
        # Login to server
        print(f"Logging in as {settings.EMAIL_HOST_USER}...")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("Login successful.")
        
        # Send test email
        print("\nSending test email...")
        send_mail(
            'YOLO System Login Verification',
            'Your verification code is: 123456',
            settings.EMAIL_HOST_USER,
            ['test@example.com'],
            fail_silently=False,
        )
        print("\n✅ Email sent successfully!")
        
        # Quit server
        server.quit()
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ SMTP Authentication Error: {e}")
        print("Possible causes:")
        print("1. Invalid email or password")
        print("2. Less secure app access not enabled")
        print("3. Two-factor authentication enabled but no app password used")
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ SMTP Connection Error: {e}")
        print("Possible causes:")
        print("1. Incorrect SMTP server address or port")
        print("2. Firewall blocking the connection")
        print("3. SMTP server unavailable")
        
    except Exception as e:
        print(f"\n❌ Email sending failed: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email()
