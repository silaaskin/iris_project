# urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import IrisViewSet

# API Router
router = DefaultRouter()
router.register(r'iris', IrisViewSet, basename='iris')

urlpatterns = [
    # Başlangıç
    path('', views.iris_list, name='iris_list'),
    
    # Iris CRUD
    path('iris/new/', views.iris_create, name='iris_create'),
    path('iris/<int:pk>/', views.iris_detail, name='iris_detail'),
    path('iris/<int:pk>/edit/', views.iris_update, name='iris_update'),
    path('iris/<int:pk>/delete/', views.iris_delete, name='iris_delete'),
    
    # Arama
    path('search/', views.iris_search, name='iris_search'),
    
    # CSV
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),
    
    # ML Tahmin
    path('predict/', views.iris_predict, name='iris_predict'),
    
    # Kullanıcı
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # API
    path('api/', include(router.urls)),
]