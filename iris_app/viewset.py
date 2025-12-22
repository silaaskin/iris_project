from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Avg, Min, Max, Count
from .models import IrisPlant, Laboratory
from .serializers import IrisPlantSerializer, LaboratorySerializer


class LaboratoryViewSet(viewsets.ModelViewSet):
    """
    Laboratory REST API
    
    Endpoints:
    - GET /api/laboratories/ - List all laboratories
    - POST /api/laboratories/ - Create new laboratory
    - GET /api/laboratories/{id}/ - Get laboratory details
    - PUT /api/laboratories/{id}/ - Update laboratory
    - DELETE /api/laboratories/{id}/ - Delete laboratory
    """
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class IrisViewSet(viewsets.ModelViewSet):
    """
    Iris Plant REST API with advanced features
    
    Endpoints:
    - GET /api/iris/ - List all iris samples
    - POST /api/iris/ - Create new iris sample
    - GET /api/iris/{id}/ - Get iris details
    - PUT /api/iris/{id}/ - Update iris sample
    - DELETE /api/iris/{id}/ - Delete iris sample
    - GET /api/iris/search/advanced/ - Advanced search with filters
    - GET /api/iris/statistics/list/ - Get statistics
    - GET /api/iris/{id}/similar/ - Get similar samples
    """
    
    queryset = IrisPlant.objects.all().select_related('lab', 'created_by')
    serializer_class = IrisPlantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['species', 'lab__name', 'created_by__username']
    ordering_fields = ['created_at', 'sepal_length', 'petal_length', 'species']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Automatically set created_by when creating new record"""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Update record while keeping created_by unchanged"""
        serializer.save()
    
    @action(detail=False, methods=['get'], url_path='search/advanced')
    def search_advanced(self, request):
        """
        Advanced search with multiple filter criteria
        """
        queryset = self.queryset
        
        # Species filter
        species = request.query_params.get('species')
        if species:
            queryset = queryset.filter(species=species)
        
        # Sepal length range
        min_sepal_length = request.query_params.get('min_sepal_length')
        if min_sepal_length:
            try:
                queryset = queryset.filter(sepal_length__gte=float(min_sepal_length))
            except (ValueError, TypeError):
                pass
        
        max_sepal_length = request.query_params.get('max_sepal_length')
        if max_sepal_length:
            try:
                queryset = queryset.filter(sepal_length__lte=float(max_sepal_length))
            except (ValueError, TypeError):
                pass
        
        # Sepal width range
        min_sepal_width = request.query_params.get('min_sepal_width')
        if min_sepal_width:
            try:
                queryset = queryset.filter(sepal_width__gte=float(min_sepal_width))
            except (ValueError, TypeError):
                pass
        
        max_sepal_width = request.query_params.get('max_sepal_width')
        if max_sepal_width:
            try:
                queryset = queryset.filter(sepal_width__lte=float(max_sepal_width))
            except (ValueError, TypeError):
                pass
        
        # Petal length range
        min_petal_length = request.query_params.get('min_petal_length')
        if min_petal_length:
            try:
                queryset = queryset.filter(petal_length__gte=float(min_petal_length))
            except (ValueError, TypeError):
                pass
        
        max_petal_length = request.query_params.get('max_petal_length')
        if max_petal_length:
            try:
                queryset = queryset.filter(petal_length__lte=float(max_petal_length))
            except (ValueError, TypeError):
                pass
        
        # Petal width range
        min_petal_width = request.query_params.get('min_petal_width')
        if min_petal_width:
            try:
                queryset = queryset.filter(petal_width__gte=float(min_petal_width))
            except (ValueError, TypeError):
                pass
        
        max_petal_width = request.query_params.get('max_petal_width')
        if max_petal_width:
            try:
                queryset = queryset.filter(petal_width__lte=float(max_petal_width))
            except (ValueError, TypeError):
                pass
        
        # Laboratory filter
        lab_id = request.query_params.get('lab_id')
        if lab_id:
            queryset = queryset.filter(lab_id=lab_id)
        
        # Creator user filter
        created_by_id = request.query_params.get('created_by_id')
        if created_by_id:
            queryset = queryset.filter(created_by_id=created_by_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Get statistics about Iris samples
        """
        total_stats = IrisPlant.objects.aggregate(
            total_samples=Count('id'),
            avg_sepal_length=Avg('sepal_length'),
            avg_sepal_width=Avg('sepal_width'),
            avg_petal_length=Avg('petal_length'),
            avg_petal_width=Avg('petal_width'),
            min_sepal_length=Min('sepal_length'),
            max_sepal_length=Max('sepal_length'),
            min_sepal_width=Min('sepal_width'),
            max_sepal_width=Max('sepal_width'),
            min_petal_length=Min('petal_length'),
            max_petal_length=Max('petal_length'),
            min_petal_width=Min('petal_width'),
            max_petal_width=Max('petal_width'),
        )
        
        species_stats = IrisPlant.objects.values('species').annotate(
            count=Count('id'),
            avg_sepal_length=Avg('sepal_length'),
            avg_petal_length=Avg('petal_length')
        )
        
        lab_stats = IrisPlant.objects.values('lab__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'total_statistics': total_stats,
            'species_distribution': list(species_stats),
            'laboratory_distribution': list(lab_stats)
        })
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """
        Get similar iris samples
        """
        try:
            iris = self.get_object()
        except IrisPlant.DoesNotExist:
            return Response(
                {'error': 'Iris sample not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        similar = IrisPlant.objects.filter(
            species=iris.species
        ).exclude(id=iris.id)[:10]
        
        serializer = self.get_serializer(similar, many=True)
        return Response({
            'reference_species': iris.get_species_display(),
            'similar_count': len(similar),
            'similar_samples': serializer.data
        })