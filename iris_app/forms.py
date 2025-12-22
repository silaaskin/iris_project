from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import IrisPlant, Laboratory


class RegisterForm(UserCreationForm):
    """Kullanıcı kayıt formu"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'E-posta adresi',
            'type': 'email'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ad'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Soyadı'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Kullanıcı adı'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Şifre',
            'type': 'password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Şifre (Tekrar)',
            'type': 'password'
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanılmakta.')
        return email


class IrisForm(forms.ModelForm):
    """Iris verilerini eklemek/düzenlemek için form"""
    class Meta:
        model = IrisPlant
        fields = ('sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species', 'lab')
        widgets = {
            'sepal_length': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Sepal Uzunluğu (cm)',
                'type': 'number'
            }),
            'sepal_width': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Sepal Genişliği (cm)',
                'type': 'number'
            }),
            'petal_length': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Petal Uzunluğu (cm)',
                'type': 'number'
            }),
            'petal_width': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Petal Genişliği (cm)',
                'type': 'number'
            }),
            'species': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lab': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        sepal_length = cleaned_data.get('sepal_length')
        sepal_width = cleaned_data.get('sepal_width')
        petal_length = cleaned_data.get('petal_length')
        petal_width = cleaned_data.get('petal_width')
        
        # Tüm değerlerin pozitif olduğunu kontrol et
        for value in [sepal_length, sepal_width, petal_length, petal_width]:
            if value is not None and value < 0:
                raise forms.ValidationError('Ölçüm değerleri negatif olamaz.')
        
        return cleaned_data


class IrisSearchForm(forms.Form):
    """Iris verileri arama formu - 3+ alan"""
    SPECIES_CHOICES = [('', '--- Tümü ---')] + list(IrisPlant.SPECIES_CHOICES)
    
    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Tür'
    )
    
    min_sepal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Min Sepal Uzunluğu (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Min Sepal Uzunluğu'
    )
    
    max_sepal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Max Sepal Uzunluğu (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Max Sepal Uzunluğu'
    )
    
    min_petal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Min Petal Uzunluğu (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Min Petal Uzunluğu'
    )
    
    max_petal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Max Petal Uzunluğu (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Max Petal Uzunluğu'
    )
    
    lab = forms.ModelChoiceField(
        queryset=Laboratory.objects.all(),
        required=False,
        empty_label='--- Tüm Laboratuvarlar ---',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Laboratuvar'
    )


class IrisImportForm(forms.Form):
    """CSV dosyasını içe aktarmak için form"""
    csv_file = forms.FileField(
        label='CSV Dosyası',
        widget=forms.FileInput(attrs={
            'class': 'form-file',
            'accept': '.csv'
        }),
        help_text='sepal_length, sepal_width, petal_length, petal_width, species sütunlarını içeren CSV dosyası'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError('Lütfen .csv dosyası yükleyin.')
            if csv_file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Dosya 5MB\'dan küçük olmalı.')
        return csv_file


class IrisPredictionForm(forms.Form):
    """Makine öğrenmesi tahminleri için form"""
    ALGORITHM_CHOICES = [
        ('logistic', 'Logistic Regression'),
        ('knn', 'K-Nearest Neighbors (KNN)'),
        ('svc', 'Support Vector Machine (SVM)'),
    ]
    
    sepal_length = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Sepal Uzunluğu (cm)',
            'type': 'number'
        }),
        label='Sepal Uzunluğu (cm)'
    )
    
    sepal_width = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Sepal Genişliği (cm)',
            'type': 'number'
        }),
        label='Sepal Genişliği (cm)'
    )
    
    petal_length = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Petal Uzunluğu (cm)',
            'type': 'number'
        }),
        label='Petal Uzunluğu (cm)'
    )
    
    petal_width = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Petal Genişliği (cm)',
            'type': 'number'
        }),
        label='Petal Genişliği (cm)'
    )
    
    algorithm = forms.ChoiceField(
        choices=ALGORITHM_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio'
        }),
        label='Tahmin Algoritması'
    )