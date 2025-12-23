from django.contrib import admin
from .models import IrisPlant, Laboratory


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    """Admin View for Laboratory Model"""
    list_display = ('name', 'city', 'country', 'phone', 'iris_count', 'created_at')
    list_filter = ('city', 'country', 'created_at')
    search_fields = ('name', 'city', 'email')
    readonly_fields = ('created_at', 'updated_at', 'iris_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'country', 'established_year')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('System Information', {
            'fields': ('iris_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def iris_count(self, obj):
        """Show count of Iris samples in this laboratory"""
        count = obj.iris_plants.count()
        return f"{count} samples"
    iris_count.short_description = "Iris Sample Count"


@admin.register(IrisPlant)
class IrisPlantAdmin(admin.ModelAdmin):
    """Admin View for Iris Plant Model"""
    list_display = ('get_species_display', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'lab', 'created_by', 'created_at')
    list_filter = ('species', 'lab', 'created_by', 'created_at')
    search_fields = ('species', 'lab__name', 'created_by__username')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Species', {
            'fields': ('species',)
        }),
        ('Measurements (cm)', {
            'fields': ('sepal_length', 'sepal_width', 'petal_length', 'petal_width'),
            'description': 'All measurements must be in centimeters (cm)'
        }),
        ('Laboratory', {
            'fields': ('lab',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by when creating a new record"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)