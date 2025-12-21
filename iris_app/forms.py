from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import IrisPlant

# Kayıt Formu
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email"]

# Çiçek Ekleme/Düzenleme Formu (Views'da hata veren kısım burasıydı)
class IrisForm(forms.ModelForm):
    class Meta:
        model = IrisPlant
        fields = ['lab', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']