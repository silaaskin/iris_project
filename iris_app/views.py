from django.shortcuts import render
from .forms import IrisForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.datasets import load_iris
import numpy as np

def iris_create(request):
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iris_list') # Kayıt sonrası listeye dön
    else:
        form = IrisForm()
    return render(request, 'iris_app/iris_form.html', {'form': form})

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

def iris_predict(request):
    prediction = None
    algorithm = request.GET.get('algorithm', 'logistic') # Varsayılan algoritma
    
    if request.GET.get('sepal_length'):
        # Iris veri setini yüklüyoruz (Eğitim için)
        iris = load_iris()
        X, y = iris.data, iris.target
        
        # Algoritma seçimi (Ödev 3 farklı seçenek istiyor)
        if algorithm == 'knn':
            model = KNeighborsClassifier(n_neighbors=3)
        elif algorithm == 'svc':
            model = SVC()
        else:
            model = LogisticRegression(max_iter=200)
            
        model.fit(X, y) # Modeli eğit
        
        # Kullanıcının girdiği verileri al
        user_data = np.array([[
            float(request.GET.get('sepal_length')),
            float(request.GET.get('sepal_width')),
            float(request.GET.get('petal_length')),
            float(request.GET.get('petal_width'))
        ]])
        
        res = model.predict(user_data)
        prediction = iris.target_names[res[0]]
        
    return render(request, 'iris_app/predict.html', {'prediction': prediction})