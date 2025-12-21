from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import IrisPlant

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email"]

class IrisForm(forms.ModelForm):
    class Meta:
        model = IrisPlant
        fields = ['lab', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']