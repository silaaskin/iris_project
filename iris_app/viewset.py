from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import IrisPlant, Laboratory
from .serializers import IrisPlantSerializer, LaboratorySerializer


class IrisViewSet(viewsets.ModelViewSet):
    """
    Iris Bitkisi REST API
    
    Endpoints:
    - GET /api/iris/ - Tüm Iris örneklerini getir
    - POST /api/iris/ - Yeni Iris örneği oluştur
    - GET /api/iris/{id}/ - Belirli Iris örneğini getir
    - PUT /api/iris/{id}/ - Iris örneğini güncelle
    - DELETE /api/iris/{id}/ - Iris örneğini sil
    - GET /api/iris/search/advanced/ - Gelişmiş arama
    """
    
    queryset = IrisPlant.objects.all().select_related('lab', 'created_by')
    serializer_class = IrisPlantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['species', 'lab__name']
    ordering_fields = ['created_at', 'sepal_length', 'petal_length']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Yeni kayıt oluştururken created_by'ı set et"""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Güncelleme yaparken created_by değişmez"""
        serializer.save()
    
    @action(detail=False, methods=['get'], url_path='search/advanced')
    def search_advanced(self, request):
        """
        Gelişmiş arama endpoint'i
        
        Query Parameters:
        - species: Iris türü (setosa, versicolor, virginica)
        - min_sepal_length: Minimum sepal uzunluğu
        - max_sepal_length: Maximum sepal uzunluğu
        - min_petal_length: Minimum petal uzunluğu
        - max_petal_length: Maximum petal uzunluğu
        - lab_id: Laboratuvar ID'si
        
        Örnek: GET /api/iris/search/advanced/?species=setosa&min_sepal_length=4.5
        """
        queryset = self.queryset
        
        # Species filtresi
        species = request.query_params.get('species')
        if species:
            queryset = queryset.filter(species=species)
        
        # Sepal length range filtresi
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
        
        # Petal length range filtresi
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
        
        # Lab filtresi
        lab_id = request.query_params.get('lab_id')
        if lab_id:
            queryset = queryset.filter(lab_id=lab_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        İstatistik endpoint'i
        Iris örneklerine dair genel istatistikler döndürür
        """
        from django.db.models import Avg, Min, Max, Count
        
        stats = IrisPlant.objects.aggregate(
            total_samples=Count('id'),
            avg_sepal_length=Avg('sepal_length'),
            avg_sepal_width=Avg('sepal_width'),
            avg_petal_length=Avg('petal_length'),
            avg_petal_width=Avg('petal_width'),
            min_sepal_length=Min('sepal_length'),
            max_sepal_length=Max('sepal_length'),
            min_petal_length=Min('petal_length'),
            max_petal_length=Max('petal_length'),
        )
        
        # Tür bazında sayım
        species_count = IrisPlant.objects.values('species').annotate(count=Count('id'))
        
        return Response({
            'statistics': stats,
            'species_distribution': list(species_count)
        })
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """
        Benzer örnekler endpoint'i
        Seçilen örneğe benzer Iris'leri döndürür
        """
        try:
            iris = self.get_object()
        except IrisPlant.DoesNotExist:
            return Response(
                {'error': 'Iris örneği bulunamadı'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Aynı türde olanları bul
        similar = IrisPlant.objects.filter(
            species=iris.species
        ).exclude(id=iris.id)[:10]
        
        serializer = self.get_serializer(similar, many=True)
        return Response(serializer.data)