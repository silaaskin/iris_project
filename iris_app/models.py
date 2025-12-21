from django.db import models
from django.contrib.auth.models import User

# Migration dosyanla uyumlu olması için Laboratory ve IrisPlant kullanmalıyız.
class Laboratory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Laboratuvar Adı")
    city = models.CharField(max_length=50, verbose_name="Şehir")

    def __str__(self):
        return self.name

class IrisPlant(models.Model):
    sepal_length = models.FloatField(verbose_name="Çanak Yaprak Uzunluğu (cm)")
    sepal_width = models.FloatField(verbose_name="Çanak Yaprak Genişliği (cm)")
    petal_length = models.FloatField(verbose_name="Taç Yaprak Uzunluğu (cm)")
    petal_width = models.FloatField(verbose_name="Taç Yaprak Genişliği (cm)")
    species = models.CharField(max_length=50, verbose_name="Tür", blank=True, null=True)
    
    lab = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="İlgili Laboratuvar")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species} ({self.id})"