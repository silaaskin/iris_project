from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Laboratory(models.Model):
    """
    Laboratuvar modeli - İkinci model olarak hizmet eder
    Many-to-One ilişkisi: Bir laboratuvarda birçok Iris örneği olabilir
    """
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
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-posta"
    )
    country = models.CharField(
        max_length=50,
        default="Turkey",
        verbose_name="Ülke"
    )
    established_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Kuruluş Yılı"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        ordering = ['name']
        verbose_name = 'Laboratuvar'
        verbose_name_plural = 'Laboratuvarlar'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def iris_count(self):
        """Bu laboratuvardaki Iris sayısını döndür"""
        return self.iris_plants.count()


class IrisPlant(models.Model):
    """
    Iris bitki verilerini depolayan ana model
    UCI Iris Dataset'ine uygun şekilde tasarlandı
    ForeignKey ile Laboratory'ye bağlı (Many-to-One ilişki)
    """
    SPECIES_CHOICES = [
        ('setosa', 'Iris Setosa'),
        ('versicolor', 'Iris Versicolor'),
        ('virginica', 'Iris Virginica'),
    ]
    
    # Ölçüm Alanları
    sepal_length = models.FloatField(
        verbose_name="Sepal Uzunluğu (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Sepal yapraklarının uzunluğu (santimetre cinsinden)"
    )
    sepal_width = models.FloatField(
        verbose_name="Sepal Genişliği (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Sepal yapraklarının genişliği (santimetre cinsinden)"
    )
    petal_length = models.FloatField(
        verbose_name="Petal Uzunluğu (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Petal yapraklarının uzunluğu (santimetre cinsinden)"
    )
    petal_width = models.FloatField(
        verbose_name="Petal Genişliği (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Petal yapraklarının genişliği (santimetre cinsinden)"
    )
    
    # Tür Alanı
    species = models.CharField(
        max_length=50,
        choices=SPECIES_CHOICES,
        verbose_name="Tür",
        help_text="Iris bitki türü (setosa, versicolor veya virginica)"
    )
    
    # İlişki Alanları
    lab = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Laboratuvar",
        related_name='iris_plants',
        help_text="Bu örneğin kaynağı olan laboratuvar"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Oluşturan Kullanıcı",
        related_name='iris_plants',
        help_text="Bu kaydı oluşturan kullanıcı"
    )
    
    # Tarih Alanları
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncellenme Tarihi"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Iris Örneği'
        verbose_name_plural = 'Iris Örnekleri'
        indexes = [
            models.Index(fields=['species']),
            models.Index(fields=['created_at']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.get_species_display()} - {self.sepal_length}cm x {self.sepal_width}cm"
    
    def get_species_display_tr(self):
        """Türün Türkçe adını döndür"""
        return dict(self.SPECIES_CHOICES).get(self.species, self.species)