from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()
router.register(r'plants', views.IrisViewSet)

urlpatterns = [
    path('', views.iris_list, name='iris_list'),
    path('iris/new/', views.iris_create, name='iris_create'),
    path('iris/update/<int:pk>/', views.iris_update, name='iris_update'),
    path('iris/delete/<int:pk>/', views.iris_delete, name='iris_delete'),
    
    # Arama ve CSV
    path('search/', views.iris_search, name='iris_search'),
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),
    
    # ML ve Kullanıcı
    path('predict/', views.iris_predict, name='iris_predict'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # API
    path('api/', include(router.urls)),
]