from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Laboratory(models.Model):
    """
    Laboratory model - Serves as the second model
    Many-to-One relationship: One laboratory can have multiple Iris samples
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Laboratory Name",
        unique=True
    )
    city = models.CharField(
        max_length=50,
        verbose_name="City"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    country = models.CharField(
        max_length=50,
        default="Turkey",
        verbose_name="Country"
    )
    established_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Established Year"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['name']
        verbose_name = 'Laboratory'
        verbose_name_plural = 'Laboratories'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def iris_count(self):
        """Returns the count of Iris samples in this laboratory"""
        return self.iris_plants.count()


class IrisPlant(models.Model):
    """
    Main model storing Iris plant data
    Designed according to the UCI Iris Dataset
    Connected to Laboratory via ForeignKey (Many-to-One relationship)
    """
    SPECIES_CHOICES = [
        ('setosa', 'Iris Setosa'),
        ('versicolor', 'Iris Versicolor'),
        ('virginica', 'Iris Virginica'),
    ]
    
    sepal_length = models.FloatField(
        verbose_name="Sepal Length (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Length of the sepal (in cm)"
    )
    sepal_width = models.FloatField(
        verbose_name="Sepal Width (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Width of the sepal (in cm)"
    )
    petal_length = models.FloatField(
        verbose_name="Petal Length (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Length of the petal (in cm)"
    )
    petal_width = models.FloatField(
        verbose_name="Petal Width (cm)",
        validators=[MinValueValidator(0.0)],
        help_text="Width of the petal (in cm)"
    )
    
    species = models.CharField(
        max_length=50,
        choices=SPECIES_CHOICES,
        verbose_name="Species",
        help_text="Iris plant species (setosa, versicolor or virginica)"
    )
    
    lab = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Laboratory",
        related_name='iris_plants',
        help_text="Source laboratory of this sample"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Created By",
        related_name='iris_plants',
        help_text="User who created this record"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Iris Sample'
        verbose_name_plural = 'Iris Samples'
        indexes = [
            models.Index(fields=['species']),
            models.Index(fields=['created_at']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.get_species_display()} - {self.sepal_length}cm x {self.sepal_width}cm"
    
    def get_species_display_tr(self):
        """Returns the display name of the species"""
        return dict(self.SPECIES_CHOICES).get(self.species, self.species)