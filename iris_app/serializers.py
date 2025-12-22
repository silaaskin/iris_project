from rest_framework import serializers
from .models import IrisPlant, Laboratory


class LaboratorySerializer(serializers.ModelSerializer):
    """Laboratory model serializer"""
    iris_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Laboratory
        fields = (
            'id', 'name', 'city', 'country', 'phone', 'email',
            'established_year', 'description', 'iris_count',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'iris_count', 'created_at', 'updated_at')
    
    def get_iris_count(self, obj):
        """Return count of iris samples in this laboratory"""
        return obj.iris_plants.count()


class IrisPlantSerializer(serializers.ModelSerializer):
    """Iris Plant model serializer with related field information"""
    
    lab_name = serializers.CharField(source='lab.name', read_only=True)
    lab_city = serializers.CharField(source='lab.city', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_fullname = serializers.SerializerMethodField()
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    lab_detail = LaboratorySerializer(source='lab', read_only=True)
    
    class Meta:
        model = IrisPlant
        fields = (
            'id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width',
            'species', 'species_display', 'lab', 'lab_name', 'lab_city', 'lab_detail',
            'created_by', 'created_by_username', 'created_by_fullname', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'species_display', 'lab_name', 'lab_city', 'lab_detail',
            'created_by_username', 'created_by_fullname', 'created_at', 'updated_at'
        )
    
    def get_created_by_fullname(self, obj):
        """Return full name of user who created this record"""
        if obj.created_by.first_name and obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return obj.created_by.username
    
    def create(self, validated_data):
        """Automatically set created_by when creating new iris sample"""
        if 'request' in self.context:
            validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, data):
        """Validate measurement data"""
        sepal_length = data.get('sepal_length')
        sepal_width = data.get('sepal_width')
        petal_length = data.get('petal_length')
        petal_width = data.get('petal_width')
        
        for value, field_name in [
            (sepal_length, 'sepal_length'),
            (sepal_width, 'sepal_width'),
            (petal_length, 'petal_length'),
            (petal_width, 'petal_width')
        ]:
            if value is not None and value < 0:
                raise serializers.ValidationError({
                    field_name: 'Measurement values cannot be negative.'
                })
        
        return data