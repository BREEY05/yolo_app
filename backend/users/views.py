from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
import json
import random
import string

# Helper to generate random code
def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

from django.conf import settings

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            print(f"Send code request received: {email}")
            
            if not email:
                print("Email is required")
                return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)
            
            code = generate_code()
            print(f"Generated code {code} for email {email}")
            
            # Store code in session
            request.session['verification_code'] = code
            request.session['verification_email'] = email
            request.session.set_expiry(300) # 5 minutes expiry
            print(f"Stored code in session: email={email}, code={code}")
            
            # Send email (commented for testing)
            try:
                send_mail(
                    'YOLO System Login Verification',
                    f'Your verification code is: {code}',
                    settings.EMAIL_HOST_USER, # Use configured sender
                    [email],
                    fail_silently=False,
                )
                print(f"Email sent successfully to {email}")
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            # Send verification code without returning it in response for security
            return JsonResponse({'status': 'success', 'message': 'Verification code sent'})
                
        except Exception as e:
            print(f"Send code error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    print("Invalid method for send code")
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def register_with_code(request):
    if request.method == 'POST':
        try:
            # Log request body for debugging
            print(f"Request body: {request.body}")
            print(f"Content type: {request.content_type}")
            print(f"Request headers: {dict(request.headers)}")
            print(f"Session ID: {request.session.session_key if request.session.session_key else 'No session'}")
            print(f"Cookies: {request.COOKIES}")
            
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            code = data.get('code')
            print(f"Register attempt: username={username}, email={email}, code={code}")
            
            if not username or not email or not code:
                print("Username, email and code are required")
                return JsonResponse({'status': 'error', 'message': 'Username, email and code are required'}, status=400)
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                print(f"Username {username} already exists")
                return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)
            
            if User.objects.filter(email=email).exists():
                print(f"Email {email} already exists")
                return JsonResponse({'status': 'error', 'message': 'Email already exists'}, status=400)
            
            # Verify code from session
            session_code = request.session.get('verification_code')
            session_email = request.session.get('verification_email')
            print(f"Session data: session_email={session_email}, session_code={session_code}")
            
            if not session_code or not session_email:
                print("No verification code found in session")
                return JsonResponse({'status': 'error', 'message': 'Verification code expired or not found. Please request a new code.'}, status=400)
            
            if email != session_email:
                print(f"Email mismatch: {email} != {session_email}")
                return JsonResponse({'status': 'error', 'message': 'Email does not match the one used to request the verification code.'}, status=400)
            
            if code != session_code:
                print(f"Code mismatch: {code} != {session_code}")
                return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'}, status=400)
            
            print(f"Verification successful for email: {email}")
            
            # Extract password from request
            password = data.get('password')
            if not password:
                print("Password is required")
                return JsonResponse({'status': 'error', 'message': 'Password is required'}, status=400)
            
            # Create new user with password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"Created new user: {username} (email: {email})")
            
            # Clear session code if it exists
            if 'verification_code' in request.session:
                del request.session['verification_code']
            if 'verification_email' in request.session:
                del request.session['verification_email']
            print(f"Cleared session for email {email}")
            
            # Return success message
            return JsonResponse({'status': 'success', 'message': 'Registration successful', 'username': username})
            
        except Exception as e:
            print(f"Registration error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    print("Invalid method for registration")
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def login_with_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(f"Login attempt: email={email}")
            
            if not email or not password:
                print("Email and password are required")
                return JsonResponse({'status': 'error', 'message': 'Email and password are required'}, status=400)
            
            # Try to find user by email
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                print(f"User not found: {email}")
                return JsonResponse({'status': 'error', 'message': 'User not found. Please register first.'}, status=404)
            
            # Check password
            if not user.check_password(password):
                print(f"Invalid password for user: {email}")
                return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=401)
            
            # Login user
            login(request, user)
            print(f"Login successful for user: {email} (username: {user.username})")
            
            # Return success message
            return JsonResponse({'status': 'success', 'message': 'Login successful', 'username': user.username})
            
        except Exception as e:
            print(f"Login error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    print("Invalid method for login")
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
