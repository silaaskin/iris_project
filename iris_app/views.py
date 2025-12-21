from django.shortcuts import render, redirect, get_object_or_404
from .forms import IrisForm, RegisterForm
from .models import IrisPlant
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Bonus kısmı için gerekli kütüphaneler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.datasets import load_iris
import numpy as np

# 1. LİSTELEME SAYFASI (Ana Sayfa)
def iris_list(request):
    samples = IrisPlant.objects.all()
    return render(request, 'iris_app/iris_list.html', {'samples': samples})

# 2. EKLEME SAYFASI
@login_required
def iris_create(request):
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.created_by = request.user # Kaydı kimin eklediğini kaydet
            plant.save()
            return redirect('iris_list')
    else:
        form = IrisForm()
    return render(request, 'iris_app/iris_form.html', {'form': form, 'title': 'Yeni Kayıt Ekle'})

# 3. GÜNCELLEME SAYFASI
@login_required
def iris_update(request, pk):
    plant = get_object_or_404(IrisPlant, pk=pk)
    if request.method == "POST":
        form = IrisForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('iris_list')
    else:
        form = IrisForm(instance=plant)
    return render(request, 'iris_app/iris_form.html', {'form': form, 'title': 'Kaydı Düzenle'})

# 4. SİLME İŞLEMİ (Sayfası yok, direkt siler)
@login_required
def iris_delete(request, pk):
    plant = get_object_or_404(IrisPlant, pk=pk)
    plant.delete()
    return redirect('iris_list')

# --- KULLANICI İŞLEMLERİ ---
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('iris_list')
    else:
        form = RegisterForm()
    return render(request, "iris_app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('iris_list')
    else:
        form = AuthenticationForm()
    return render(request, "iris_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- BONUS: TAHMİN (PREDICT) ---
def iris_predict(request):
    prediction = None
    algorithm = request.GET.get('algorithm', 'logistic')
    
    if request.GET.get('sepal_length'):
        iris = load_iris()
        X, y = iris.data, iris.target
        
        if algorithm == 'knn':
            model = KNeighborsClassifier(n_neighbors=3)
        elif algorithm == 'svc':
            model = SVC()
        else:
            model = LogisticRegression(max_iter=200)
            
        model.fit(X, y)
        
        user_data = np.array([[
            float(request.GET.get('sepal_length')),
            float(request.GET.get('sepal_width')),
            float(request.GET.get('petal_length')),
            float(request.GET.get('petal_width'))
        ]])
        
        res = model.predict(user_data)
        prediction = iris.target_names[res[0]]
        
    return render(request, 'iris_app/predict.html', {'prediction': prediction})