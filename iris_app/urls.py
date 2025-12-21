from django.urls import path
from . import views

urlpatterns = [
    path('', views.iris_list, name='iris_list'),
    path('iris/<int:pk>/', views.iris_detail, name='iris_detail'),
    path('iris/new/', views.iris_create, name='iris_create'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('predict/', views.iris_predict, name='iris_predict'),
]