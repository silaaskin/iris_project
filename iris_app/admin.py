from django.contrib import admin
from .models import IrisPlant, Laboratory

class IrisPlantAdmin(admin.ModelAdmin):
    list_display = ('species', 'sepal_length', 'petal_length', 'lab', 'created_at')
    list_filter = ('species', 'lab')
    search_fields = ('species',)

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')

admin.site.register(IrisPlant, IrisPlantAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)