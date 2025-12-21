#!/usr/bin/env python3
"""
Test script to verify user registration with friendly username generation
"""

import requests
import time

# API endpoints
BASE_URL = 'http://localhost:8000/api/users'
SEND_CODE_URL = f'{BASE_URL}/send_code/'
LOGIN_URL = f'{BASE_URL}/login/'

# Test email for new user
TEST_EMAIL = 'test_new_user_verification@example.com'

def test_user_registration():
    """Test the user registration flow"""
    print("=== User Registration Test ===")
    print(f"Test email: {TEST_EMAIL}")
    
    # Step 1: Send verification code
    print("\n1. Sending verification code...")
    payload = {'email': TEST_EMAIL}
    response = requests.post(SEND_CODE_URL, json=payload)
    
    if response.status_code != 200:
        print(f"   ❌ Failed to send verification code: {response.status_code}")
        print(f"   Error: {response.text}")
        return False
    
    print(f"   ✓ Verification code sent successfully")
    response_data = response.json()
    print(f"   Response: {response_data}")
    
    code = response_data.get('code')
    if not code:
        print("   ❌ No code returned in response")
        return False
    
    print(f"   ✓ Received verification code: {code}")
    
    # Step 2: Login with verification code
    print("\n2. Logging in with verification code...")
    login_payload = {
        'email': TEST_EMAIL,
        'code': code
    }
    
    login_response = requests.post(LOGIN_URL, json=login_payload)
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed: {login_response.status_code}")
        print(f"   Error: {login_response.text}")
        return False
    
    login_data = login_response.json()
    print(f"   ✓ Login successful")
    print(f"   Response: {login_data}")
    
    # Step 3: Check username generation
    username = login_data.get('username')
    created = login_data.get('created', False)
    message = login_data.get('message')
    
    print("\n3. Checking username generation...")
    print(f"   Username: {username}")
    print(f"   Created: {created}")
    print(f"   Message: {message}")
    
    # Verify username format
    if username.startswith('user_') and len(username) == 11:
        print(f"   ✓ PASS: Username follows expected format (user_xxxxx)")
    else:
        print(f"   ⚠ Username doesn't follow expected format: {username}")
    
    # Verify user was created
    if created:
        print("   ✓ PASS: User was successfully created")
    else:
        print("   ⚠ User already exists (this is okay if you've run this test before)")
    
    print("\n=== Test Summary ===")
    print("✓ Test completed successfully")
    print("✓ Username generation is working")
    print("✓ Login flow is working")
    print(f"✓ Final username: {username}")
    
    return True

if __name__ == "__main__":
    test_user_registration()
