"""
URL configuration for iris_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # <-- Yönlendirme için gerekli

urlpatterns = [
    # Admin Paneli
    path('admin/', admin.site.urls),
    
    # --- 1. HATA ÖNLEYİCİ YÖNLENDİRMELER ---
    
    # Login Hatası Çözümü:
    # Sistem 'accounts/login'e gitmeye kalkarsa, bizim '/login/'e yolla.
    path('accounts/login/', lambda request: redirect('/login/', permanent=True)),
    
    # Logout Hatası Çözümü (HTTP 405):
    # Sistem 'accounts/logout'a gitmeye kalkarsa, bizim '/logout/'a yolla.
    path('accounts/logout/', lambda request: redirect('/logout/', permanent=True)),
    
    # --- 2. UYGULAMA URL'LERİ ---
    # Login, Register, Home, CRUD işlemleri burada (iris_app/urls.py)
    path('', include('iris_app.urls')), 
    
    # --- 3. EKSTRA AUTH URL'LERİ ---
    # Sadece şifre sıfırlama (password reset) gibi özellikler için gerekli.
    # Giriş/Çıkış işlemleri zaten yukarıda 'iris_app.urls' içinde hallediliyor.
    path('accounts/', include('django.contrib.auth.urls')), 
]