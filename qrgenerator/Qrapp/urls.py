from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_qr_code/<str:data>/', views.download_qr_code, name='download_qr_code'),
    path('animated_qr/', views.animated_qr, name='animated_qr'),
    path('video_display/', views.video_display, name='video_display'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'),
]
