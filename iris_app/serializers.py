# serializers.py (REST API için)
from rest_framework import serializers
from .models import IrisPlant, Laboratory


class LaboratorySerializer(serializers.ModelSerializer):
    """Laboratuvar Serializer"""
    class Meta:
        model = Laboratory
        fields = ('id', 'name', 'city', 'description', 'phone', 'created_at')
        read_only_fields = ('id', 'created_at')


class IrisPlantSerializer(serializers.ModelSerializer):
    """Iris Bitki Serializer"""
    lab_name = serializers.CharField(source='lab.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    
    class Meta:
        model = IrisPlant
        fields = (
            'id',
            'sepal_length',
            'sepal_width',
            'petal_length',
            'petal_width',
            'species',
            'species_display',
            'lab',
            'lab_name',
            'created_by',
            'created_by_username',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """Yeni kayıt oluştururken created_by'ı otomatik set et"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)