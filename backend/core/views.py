from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .detector import YOLODetector
from .camera_utils import get_available_cameras
import os
import subprocess
import sys
import json
from werkzeug.utils import secure_filename

# Paths
BASE_DIR = settings.BASE_DIR
MODELS_DIR = os.path.join(BASE_DIR, 'models')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# Initialize Detector
default_model = os.path.join(MODELS_DIR, 'yolov8n.pt')
if not os.path.exists(default_model):
    existing_models = [f for f in os.listdir(MODELS_DIR) if f.endswith('.pt')]
    if existing_models:
        default_model = os.path.join(MODELS_DIR, existing_models[0])

detector = YOLODetector(default_model)

def open_folder_dialog():
    """
    Opens a folder selection dialog using Tkinter directly (since we are not frozen yet, or similar to Flask fix)
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askdirectory()
        root.destroy()
        return path
    except Exception as e:
        print(f"Error opening dialog: {e}")
        return ""

def get_models(request):
    models = []
    if os.path.exists(MODELS_DIR):
        for f in os.listdir(MODELS_DIR):
            if f.endswith('.pt'):
                models.append(f)
    return JsonResponse({'models': models})

@csrf_exempt
def set_model(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        model_name = data.get('model_name')
        model_path = os.path.join(MODELS_DIR, model_name)
        if detector.load_model(model_path):
            return JsonResponse({'status': 'success', 'message': f'Loaded {model_name}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Model not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def upload_model(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part'}, status=400)
        file = request.FILES['file']
        if file.name == '':
            return JsonResponse({'error': 'No selected file'}, status=400)
        
        if not file.name.endswith('.pt'):
            return JsonResponse({'error': 'Invalid file type. Only .pt files allowed'}, status=400)

        filename = secure_filename(file.name)
        filepath = os.path.join(MODELS_DIR, filename)
        with open(filepath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return JsonResponse({'status': 'success', 'message': f'Model {filename} uploaded'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def get_cameras_view(request):
    cameras = get_available_cameras()
    return JsonResponse({'cameras': cameras})

def select_folder(request):
    path = open_folder_dialog()
    if path:
        return JsonResponse({'path': path})
    else:
        return JsonResponse({'path': ''}, status=400)

@csrf_exempt
def upload_temp(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part'}, status=400)
        file = request.FILES['file']
        if file.name == '':
            return JsonResponse({'error': 'No selected file'}, status=400)
        
        filename = secure_filename(file.name)
        filepath = os.path.join(TEMP_DIR, filename)
        with open(filepath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return JsonResponse({'filename': filename})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def process_stream(request, filename):
    save_dir = request.GET.get('save_path')
    if not save_dir or not os.path.exists(save_dir):
        return JsonResponse({'error': 'Invalid save path'}, status=400)
    
    filepath = os.path.join(TEMP_DIR, secure_filename(filename))
    if not os.path.exists(filepath):
        return JsonResponse({'error': 'File not found'}, status=404)

    # Determine if image or video
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        return StreamingHttpResponse(detector.process_image_file(filepath, save_dir),
                        content_type='multipart/x-mixed-replace; boundary=frame')
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        return StreamingHttpResponse(detector.process_video_file(filepath, save_dir),
                        content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return JsonResponse({'error': 'Unsupported file type'}, status=400)

def camera_feed(request, camera_id):
    return StreamingHttpResponse(detector.process_camera(camera_id),
                    content_type='multipart/x-mixed-replace; boundary=frame')
