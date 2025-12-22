# admin.py
from django.contrib import admin
from .models import IrisPlant, Laboratory

@admin.register(IrisPlant)
class IrisPlantAdmin(admin.ModelAdmin):
    """Iris Bitki Modeli Admin Paneli"""
    list_display = ('get_species_display', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'lab', 'created_by', 'created_at')
    list_filter = ('species', 'lab', 'created_at', 'created_by')
    search_fields = ('species', 'lab__name')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Türü', {
            'fields': ('species',)
        }),
        ('Ölçümler (cm)', {
            'fields': ('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
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


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    """Laboratuvar Modeli Admin Paneli"""
    list_display = ('name', 'city', 'phone', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('name', 'city')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'city')
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone',)
        }),
        ('Açıklama', {
            'fields': ('description',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )