from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import IrisPlant, Laboratory


class RegisterForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
            'type': 'email'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username',
                'type': 'text'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'type': 'password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'type': 'password'
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class IrisForm(forms.ModelForm):
    """Form for adding/editing Iris data"""
    class Meta:
        model = IrisPlant
        fields = ('sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species', 'lab')
        widgets = {
            'sepal_length': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Sepal Length (cm)',
                'type': 'number'
            }),
            'sepal_width': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Sepal Width (cm)',
                'type': 'number'
            }),
            'petal_length': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Petal Length (cm)',
                'type': 'number'
            }),
            'petal_width': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Petal Width (cm)',
                'type': 'number'
            }),
            'species': forms.Select(attrs={
                'class': 'form-input'
            }),
            'lab': forms.Select(attrs={
                'class': 'form-input'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        sepal_length = cleaned_data.get('sepal_length')
        sepal_width = cleaned_data.get('sepal_width')
        petal_length = cleaned_data.get('petal_length')
        petal_width = cleaned_data.get('petal_width')
        
        for value in [sepal_length, sepal_width, petal_length, petal_width]:
            if value is not None and value < 0:
                raise forms.ValidationError('Measurement values cannot be negative.')
        
        return cleaned_data


class IrisSearchForm(forms.Form):
    """Iris data search form"""
    SPECIES_CHOICES = [('', '--- All Species ---')] + list(IrisPlant.SPECIES_CHOICES)
    
    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input'
        }),
        label='Species'
    )
    
    min_sepal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Min Sepal Length (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Min Sepal Length'
    )
    
    max_sepal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Max Sepal Length (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Max Sepal Length'
    )
    
    min_petal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Min Petal Length (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Min Petal Length'
    )
    
    max_petal_length = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Max Petal Length (cm)',
            'step': '0.1',
            'type': 'number'
        }),
        label='Max Petal Length'
    )
    
    lab = forms.ModelChoiceField(
        queryset=Laboratory.objects.all(),
        required=False,
        empty_label='--- All Laboratories ---',
        widget=forms.Select(attrs={
            'class': 'form-input'
        }),
        label='Laboratory'
    )


class IrisImportForm(forms.Form):
    """Form for importing CSV files"""
    csv_file = forms.FileField(
        label='CSV File',
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': '.csv'
        }),
        help_text='CSV file must contain: sepal_length, sepal_width, petal_length, petal_width, species columns'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError('Please upload a .csv file.')
            if csv_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 5MB.')
        return csv_file


class IrisPredictionForm(forms.Form):
    """Form for machine learning predictions"""
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
            'placeholder': 'Sepal Length (cm)',
            'type': 'number'
        }),
        label='Sepal Length (cm)'
    )
    
    sepal_width = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Sepal Width (cm)',
            'type': 'number'
        }),
        label='Sepal Width (cm)'
    )
    
    petal_length = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Petal Length (cm)',
            'type': 'number'
        }),
        label='Petal Length (cm)'
    )
    
    petal_width = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.1',
            'placeholder': 'Petal Width (cm)',
            'type': 'number'
        }),
        label='Petal Width (cm)'
    )
    
    algorithm = forms.ChoiceField(
        choices=ALGORITHM_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio'
        }),
        label='Prediction Algorithm'
    )