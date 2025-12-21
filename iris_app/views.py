import csv
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import IrisForm, RegisterForm
from .models import IrisPlant

# ML Kütüphaneleri
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.datasets import load_iris

# API Kütüphaneleri
from rest_framework import viewsets, serializers

# --- API SERIALIZER & VIEWSET ---
class IrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisPlant
        fields = '__all__'

class IrisViewSet(viewsets.ModelViewSet):
    queryset = IrisPlant.objects.all()
    serializer_class = IrisSerializer

# --- CRUD İŞLEMLERİ ---
def iris_list(request):
    samples = IrisPlant.objects.all()
    return render(request, 'iris_app/iris_list.html', {'samples': samples})

@login_required
def iris_create(request):
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.created_by = request.user
            plant.save()
            return redirect('iris_list')
    else:
        form = IrisForm()
    return render(request, 'iris_app/iris_form.html', {'form': form, 'title': 'Yeni Kayıt Ekle'})

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

@login_required
def iris_delete(request, pk):
    plant = get_object_or_404(IrisPlant, pk=pk)
    plant.delete()
    return redirect('iris_list')

# --- GELİŞMİŞ ARAMA ---
def iris_search(request):
    query = request.GET.get('q', '')
    min_sepal = request.GET.get('min_sepal')
    min_petal = request.GET.get('min_petal')
    
    results = IrisPlant.objects.all()

    if query:
        results = results.filter(species__icontains=query)
    if min_sepal:
        results = results.filter(sepal_length__gte=min_sepal)
    if min_petal:
        results = results.filter(petal_length__gte=min_petal)

    return render(request, 'iris_app/search.html', {'results': results})

# --- CSV İŞLEMLERİ ---
def export_iris_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Species', 'Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width', 'Lab'])
    for plant in IrisPlant.objects.all():
        lab_name = plant.lab.name if plant.lab else "N/A"
        writer.writerow([plant.id, plant.species, plant.sepal_length, plant.sepal_width, plant.petal_length, plant.petal_width, lab_name])
    return response

@login_required
def import_iris_csv(request):
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader) # Başlığı atla
        for row in reader:
            if len(row) >= 5:
                IrisPlant.objects.create(
                    species=row[0],
                    sepal_length=float(row[1]),
                    sepal_width=float(row[2]),
                    petal_length=float(row[3]),
                    petal_width=float(row[4]),
                    created_by=request.user
                )
        return redirect('iris_list')
    return render(request, 'iris_app/import.html')

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
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('iris_list')
    else:
        form = AuthenticationForm()
    return render(request, "iris_app/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- MAKİNE ÖĞRENMESİ (BONUS) ---
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