from django.urls import path
from . import views

urlpatterns = [
    path('get_models', views.get_models, name='get_models'),
    path('set_model', views.set_model, name='set_model'),
    path('upload_model', views.upload_model, name='upload_model'),
    path('get_cameras', views.get_cameras_view, name='get_cameras'),
    path('select_folder', views.select_folder, name='select_folder'),
    path('upload_temp', views.upload_temp, name='upload_temp'),
    path('process_stream/<str:filename>', views.process_stream, name='process_stream'),
    path('camera_feed/<int:camera_id>', views.camera_feed, name='camera_feed'),
]
