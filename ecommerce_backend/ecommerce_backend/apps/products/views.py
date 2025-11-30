from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, ProductListSerializer, 
    ProductDetailSerializer, ProductReviewSerializer
)
from .filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'name', 'created_at', 'stock']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
        
        # Optimize queries based on action
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('images', 'reviews__user')
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, slug=None):
        product = self.get_object()
        serializer = ProductReviewSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Check if user already reviewed this product
            if ProductReview.objects.filter(product=product, user=request.user).exists():
                return Response(
                    {'error': 'You have already reviewed this product.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products (in stock and with highest ratings)"""
        try:
            featured_products = self.get_queryset().filter(
                stock__gt=0  # Only products with stock > 0
            ).annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            ).filter(
                avg_rating__gte=4.0,  # At least 4-star rating
                review_count__gte=1   # At least 1 review
            ).order_by('-avg_rating', '-review_count')[:10]  # Order by rating then review count
            
            serializer = self.get_serializer(featured_products, many=True)
            return Response({
                'count': len(featured_products),
                'results': serializer.data
            })
        except Exception as e:
            return Response(
                {'error': f'Error fetching featured products: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
