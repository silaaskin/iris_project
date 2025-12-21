from django.urls import path
from . import views

urlpatterns = [
    path('', views.iris_list, name='iris_list'),
    path('iris/new/', views.iris_create, name='iris_create'),
    path('iris/update/<int:pk>/', views.iris_update, name='iris_update'), # Düzenleme linki
    path('iris/delete/<int:pk>/', views.iris_delete, name='iris_delete'), # Silme linki
    path('predict/', views.iris_predict, name='iris_predict'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]