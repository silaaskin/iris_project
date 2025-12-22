from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Laboratory(models.Model):
    """Laboratuvar modeli - İkinci model olarak hizmet eder"""
    name = models.CharField(
        max_length=100,
        verbose_name="Laboratuvar Adı",
        unique=True
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Şehir"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Açıklama"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefon"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Laboratuvar'
        verbose_name_plural = 'Laboratuvarlar'

    def __str__(self):
        return f"{self.name} ({self.city})"


class IrisPlant(models.Model):
    """
    Iris bitki verilerini depolayan ana model.
    UCI Iris Dataset'ine uygun şekilde tasarlandı.
    """
    SPECIES_CHOICES = [
        ('setosa', 'Iris Setosa'),
        ('versicolor', 'Iris Versicolor'),
        ('virginica', 'Iris Virginica'),
    ]
    
    sepal_length = models.FloatField(
        verbose_name="Sepal Uzunluğu (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Sepal yapraklarının uzunluğu"
    )
    sepal_width = models.FloatField(
        verbose_name="Sepal Genişliği (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Sepal yapraklarının genişliği"
    )
    petal_length = models.FloatField(
        verbose_name="Petal Uzunluğu (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Petal yapraklarının uzunluğu"
    )
    petal_width = models.FloatField(
        verbose_name="Petal Genişliği (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Petal yapraklarının genişliği"
    )
    species = models.CharField(
        max_length=50,
        choices=SPECIES_CHOICES,
        verbose_name="Tür",
        help_text="Iris bitki türü"
    )
    
    # ForeignKey ile Laboratory'ye bağlantı
    lab = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Laboratuvar",
        related_name='iris_plants',
        help_text="Örneğin kaynağı olan laboratuvar"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Oluşturan Kullanıcı",
        related_name='iris_plants'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturma Tarihi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncelleme Tarihi"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Iris Örneği'
        verbose_name_plural = 'Iris Örnekleri'
        indexes = [
            models.Index(fields=['species']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_species_display()} - {self.sepal_length}cm"
    
    def get_species_display_tr(self):
        """Türün Türkçe adını döndür"""
        return dict(self.SPECIES_CHOICES).get(self.species, self.species)