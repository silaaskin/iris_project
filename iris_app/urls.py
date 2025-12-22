from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# BURAYI DÜZELTTİK: .viewsets (çoğul) yerine .viewset (tekil) yaptık
from .viewset import IrisViewSet, LaboratoryViewSet 

# REST API Router
router = DefaultRouter()
router.register(r'iris', IrisViewSet, basename='iris-api')
router.register(r'laboratories', LaboratoryViewSet, basename='lab-api')

urlpatterns = [
    # Dashboard / Ana Sayfa
    path('', views.iris_list, name='iris_list'),
    
    # Iris CRUD Operations
    path('iris/new/', views.iris_create, name='iris_create'),
    path('iris/<int:pk>/', views.iris_detail, name='iris_detail'),
    path('iris/<int:pk>/edit/', views.iris_update, name='iris_update'),
    path('iris/<int:pk>/delete/', views.iris_delete, name='iris_delete'),
    
    # Search
    path('search/', views.iris_search, name='iris_search'),
    
    # CSV Import/Export
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),
    
    # Machine Learning Prediction
    path('predict/', views.iris_predict, name='iris_predict'),
    
    # User Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # REST API Endpoints
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]