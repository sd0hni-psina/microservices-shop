from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, ProductCreateUpdateSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    serach_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

@api_view(['POST'])
def reserve_product(request, product_id):
    """Резервирует указанное количество товара."""
    try:
        product = Product.objects.get(id=product_id,)
        quantity = request.data.get('quantity', 1)

        if product.reserv_quantity(quantity):
            return Response({
                'success': True,
                'message': f'Successfully reserved {quantity} of {product.name}',
                'remaining_stock': product.stock_quantity
            })
        else:
            return Response({
                'success': False,
                'message': 'Insufficient stock',
                'available_stock': product.stock_quantity
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def release_product(request, product_id):
    """Освобождает ранее зарезервированное количество товара."""
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity', 1)
        product.release_quantity(quantity)
        return Response({
            'success': True,
            'message': f'Successfully released {quantity} of {product.name}',
            'current_stock': product.stock_quantity
        })
    
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def check_availability(request, product_id):
    """Проверяет доступность товара."""
    try:
        product = Product.objects.get(id=product_id)
        quantity = int(request.query_params.get('quantity', 1))
        return Response({
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'available': product.stock_quantity >= quantity,
            'stock_quantity': product.stock_quantity,
            'requested_quantity': quantity
        })
    
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)