from django.db import models

# 1. Model: Çiçeklerin kategorilerini tutar (Örn: Dağ Çiçekleri, Sera Çiçekleri)
class Category(models.Model):
    name = models.CharField(max_length=100) # Kategori adı
    description = models.TextField()        # Açıklama
    origin = models.CharField(max_length=100) # Kökeni
    priority = models.IntegerField(default=1) # Önem sırası
    is_active = models.BooleanField(default=True) # Aktif mi?

    def _str_(self):
        return self.name

# 2. Model: Iris verilerini tutan ana model
class IrisSample(models.Model):
    # İlişki: Her örnek bir kategoriye ait olmalı (Many-to-One)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    species = models.CharField(max_length=50) # Setosa, Versicolor, Virginica

    def _str_(self):
        return f"{self.species} ({self.id})"