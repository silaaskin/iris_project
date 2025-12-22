import csv
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import IrisForm, RegisterForm, IrisSearchForm, IrisImportForm, IrisPredictionForm
from .models import IrisPlant, Laboratory

# ============= YETKİ KONTROLÜ (HELPER) =============
def is_editor_check(user):
    """Kullanıcı Admin mi veya 'Editor' grubunda mı?"""
    return user.is_superuser or user.groups.filter(name='Editor').exists()

# ============= AUTHENTICATION VIEWS =============

def register_view(request):
    """Kullanıcı kayıt sayfası"""
    if request.user.is_authenticated:
        return redirect('iris_list')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Hoşgeldiniz {user.username}!')
            return redirect('iris_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegisterForm()
    
    return render(request, "iris_app/register.html", {"form": form})


def login_view(request):
    """Kullanıcı giriş sayfası"""
    if request.user.is_authenticated:
        return redirect('iris_list')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Hoşgeldiniz, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'iris_list'
            return redirect(next_url)
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    else:
        form = AuthenticationForm()
    
    return render(request, "iris_app/login.html", {"form": form})


def logout_view(request):
    """Çıkış işlemi"""
    logout(request)
    messages.success(request, 'Çıkış yapıldı.')
    return redirect('login')


# ============= DASHBOARD =============

@login_required(login_url='login')
def iris_list(request):
    """Ana Iris listesi sayfası"""
    samples = IrisPlant.objects.all().select_related('lab', 'created_by').order_by('-created_at')
    
    is_editor = is_editor_check(request.user)

    context = {
        'samples': samples,
        'total_count': samples.count(),
        'species_types': dict(IrisPlant.SPECIES_CHOICES) if hasattr(IrisPlant, 'SPECIES_CHOICES') else {},
        'is_editor': is_editor,
    }
    
    return render(request, 'iris_app/iris_list.html', context)


# ============= IRIS CRUD VIEWS =============

@login_required(login_url='login')
@user_passes_test(is_editor_check, login_url='login')
def iris_create(request):
    """Yeni Iris kaydı ekleme sayfası"""
    if request.method == "POST":
        form = IrisForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.created_by = request.user
            plant.save()
            messages.success(request, 'Iris örneği başarıyla eklendi.')
            return redirect('iris_detail', pk=plant.pk)
        else:
            messages.error(request, 'Lütfen tüm alanları doğru şekilde doldurun.')
    else:
        form = IrisForm()
    
    context = {
        'form': form,
        'title': 'Yeni Iris Örneği Ekle',
        'action': 'create'
    }
    
    return render(request, 'iris_app/iris_form.html', context)


@login_required(login_url='login')
def iris_detail(request, pk):
    """Iris detayını görüntüle"""
    plant = get_object_or_404(IrisPlant, pk=pk)
    
    is_editor = is_editor_check(request.user)
    
    context = {
        'plant': plant,
        'can_edit': is_editor and (plant.created_by == request.user or request.user.is_superuser)
    }
    
    return render(request, 'iris_app/iris_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_editor_check, login_url='login')
def iris_update(request, pk):
    """Iris kaydını düzenleme sayfası"""
    plant = get_object_or_404(IrisPlant, pk=pk)
    
    if plant.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Bu kaydı düzenleme yetkiniz yok.')
        return redirect('iris_list')
    
    if request.method == "POST":
        form = IrisForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iris örneği güncellendi.')
            return redirect('iris_detail', pk=plant.pk)
        else:
            messages.error(request, 'Lütfen tüm alanları doğru şekilde doldurun.')
    else:
        form = IrisForm(instance=plant)
    
    context = {
        'form': form,
        'plant': plant,
        'title': 'Iris Örneğini Düzenle',
        'action': 'update'
    }
    
    return render(request, 'iris_app/iris_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_editor_check, login_url='login')
def iris_delete(request, pk):
    """Iris kaydını silme sayfası"""
    plant = get_object_or_404(IrisPlant, pk=pk)
    
    if plant.created_by != request.user and not request.user.is_superuser:
        messages.error(request, 'Bu kaydı silme yetkiniz yok.')
        return redirect('iris_list')
    
    if request.method == "POST":
        plant_name = str(plant)
        plant.delete()
        messages.success(request, f'{plant_name} silindi.')
        return redirect('iris_list')
    
    context = {'plant': plant}
    return render(request, 'iris_app/iris_confirm_delete.html', context)


# ============= SEARCH VIEWS =============

@login_required(login_url='login')
def iris_search(request):
    """Gelişmiş arama sayfası - 3+ alan"""
    form = IrisSearchForm(request.GET or None)
    results = IrisPlant.objects.all().select_related('lab', 'created_by')
    search_performed = False
    
    if form.is_valid():
        search_performed = True
        
        species = form.cleaned_data.get('species')
        if species:
            results = results.filter(species=species)
        
        min_sepal_length = form.cleaned_data.get('min_sepal_length')
        if min_sepal_length:
            results = results.filter(sepal_length__gte=min_sepal_length)
        
        max_sepal_length = form.cleaned_data.get('max_sepal_length')
        if max_sepal_length:
            results = results.filter(sepal_length__lte=max_sepal_length)
        
        min_petal_length = form.cleaned_data.get('min_petal_length')
        if min_petal_length:
            results = results.filter(petal_length__gte=min_petal_length)
        
        max_petal_length = form.cleaned_data.get('max_petal_length')
        if max_petal_length:
            results = results.filter(petal_length__lte=max_petal_length)
        
        lab = form.cleaned_data.get('lab')
        if lab:
            results = results.filter(lab=lab)
    
    context = {
        'form': form,
        'results': results,
        'result_count': results.count(),
        'search_performed': search_performed,
    }
    
    return render(request, 'iris_app/search.html', context)


# ============= IMPORT/EXPORT VIEWS =============

@login_required(login_url='login')
@user_passes_test(is_editor_check, login_url='login')
def import_iris_csv(request):
    """CSV dosyasını içe aktarma"""
    if request.method == "POST":
        form = IrisImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                
                imported_count = 0
                error_count = 0
                
                species_dict = dict(IrisPlant.SPECIES_CHOICES) if hasattr(IrisPlant, 'SPECIES_CHOICES') else {}

                for row in reader:
                    try:
                        species = row.get('species', '').lower().strip()
                        if species_dict and species not in species_dict.keys():
                            error_count += 1
                            continue
                        
                        IrisPlant.objects.create(
                            species=species,
                            sepal_length=float(row.get('sepal_length', 0)),
                            sepal_width=float(row.get('sepal_width', 0)),
                            petal_length=float(row.get('petal_length', 0)),
                            petal_width=float(row.get('petal_width', 0)),
                            lab_id=row.get('lab_id') if row.get('lab_id') else None,
                            created_by=request.user
                        )
                        imported_count += 1
                    except (ValueError, KeyError) as e:
                        error_count += 1
                        continue
                
                if imported_count > 0:
                    messages.success(request, f'{imported_count} Iris örneği içe aktarıldı.')
                if error_count > 0:
                    messages.warning(request, f'{error_count} satır hata nedeniyle atlandı.')
                
                return redirect('iris_list')
            
            except Exception as e:
                messages.error(request, f'Dosya işlenirken hata oluştu: {str(e)}')
        else:
            messages.error(request, 'Lütfen geçerli bir CSV dosyası yükleyin.')
    else:
        form = IrisImportForm()
    
    return render(request, 'iris_app/import.html', {'form': form})


def export_iris_csv(request):
    """Iris verileri CSV olarak dışa aktar"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="iris_export.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['Tür', 'Sepal Uzunluğu', 'Sepal Genişliği', 'Petal Uzunluğu', 'Petal Genişliği', 'Laboratuvar', 'Tarih'])
    
    for plant in IrisPlant.objects.all().select_related('lab'):
        lab_name = plant.lab.name if plant.lab else "N/A"
        species_display = plant.get_species_display() if hasattr(plant, 'get_species_display') else plant.species
        
        writer.writerow([
            species_display,
            plant.sepal_length,
            plant.sepal_width,
            plant.petal_length,
            plant.petal_width,
            lab_name,
            plant.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response


# ============= MACHINE LEARNING PREDICTION (BONUS) =============

@login_required(login_url='login')
def iris_predict(request):
    """Makine öğrenmesi tahminleme sayfası - 3+ algoritma seçeneği"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.datasets import load_iris
    from sklearn.preprocessing import StandardScaler
    
    prediction = None
    confidence = None
    algorithm_name = None
    error_message = None
    
    if request.method == 'POST':
        try:
            sepal_length = float(request.POST.get('sepal_length', 0))
            sepal_width = float(request.POST.get('sepal_width', 0))
            petal_length = float(request.POST.get('petal_length', 0))
            petal_width = float(request.POST.get('petal_width', 0))
            algorithm = request.POST.get('algorithm', 'logistic')
            
            iris_data = load_iris()
            X, y = iris_data.data, iris_data.target
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            if algorithm == 'knn':
                model = KNeighborsClassifier(n_neighbors=3)
                algorithm_name = 'K-Nearest Neighbors (KNN)'
            elif algorithm == 'svc':
                model = SVC(probability=True)
                algorithm_name = 'Support Vector Machine (SVM)'
            else:
                model = LogisticRegression(max_iter=200, random_state=42)
                algorithm_name = 'Logistic Regression'
            
            model.fit(X_scaled, y)
            
            user_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            user_data_scaled = scaler.transform(user_data)
            
            prediction_idx = model.predict(user_data_scaled)[0]
            prediction = iris_data.target_names[prediction_idx]
            
            if hasattr(model, 'predict_proba'):
                prob = float(max(model.predict_proba(user_data_scaled)[0]))
                confidence = int(round(prob * 100))
                confidence = max(0, min(100, confidence))
            
        except ValueError:
            error_message = 'Lütfen tüm ölçüm alanlarına sayı girin.'
        except Exception as e:
            error_message = f'Tahmin sırasında hata oluştu: {str(e)}'
    
    context = {
        'prediction': prediction,
        'confidence': confidence if confidence is not None else None,
        'algorithm_name': algorithm_name,
        'error_message': error_message,
    }
    
    return render(request, 'iris_app/predict.html', context)