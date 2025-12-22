from django.contrib import admin
from .models import IrisPlant, Laboratory


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    """Laboratuvar Modeli Admin Paneli"""
    list_display = ('name', 'city', 'country', 'phone', 'iris_count', 'created_at')
    list_filter = ('city', 'country', 'created_at')
    search_fields = ('name', 'city', 'email')
    readonly_fields = ('created_at', 'updated_at', 'iris_count')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'city', 'country', 'established_year')
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'email')
        }),
        ('Açıklama', {
            'fields': ('description',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('iris_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def iris_count(self, obj):
        """Bu laboratuvardaki Iris örnek sayısını göster"""
        count = obj.iris_plants.count()
        return f"{count} örnek"
    iris_count.short_description = "Iris Örnek Sayısı"


@admin.register(IrisPlant)
class IrisPlantAdmin(admin.ModelAdmin):
    """Iris Bitki Modeli Admin Paneli"""
    list_display = ('get_species_display', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'lab', 'created_by', 'created_at')
    list_filter = ('species', 'lab', 'created_by', 'created_at')
    search_fields = ('species', 'lab__name', 'created_by__username')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Türü', {
            'fields': ('species',)
        }),
        ('Ölçümler (cm)', {
            'fields': ('sepal_length', 'sepal_width', 'petal_length', 'petal_width'),
            'description': 'Tüm ölçümler santimetre (cm) cinsinden olmalıdır'
        }),
        ('Laboratuvar', {
            'fields': ('lab',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Yeni kayıt oluştururken created_by'ı otomatik set et"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)