from django.shortcuts import render

from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # AllowAny permission to allow unauthenticated access

from django_filters.rest_framework import DjangoFilterBackend # Django filter backend for filtering capabilities

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer

# Create your views here.
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny] # Allow anyone to view product categories

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True).order_by('name') # Only available products by default
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] # Allow anyone to view products, but restrict creation to staff

    # Filters and Search for product retrieval
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'price', 'is_available'] 
    search_fields = ['name', 'description', 'category__name'] 
    ordering_fields = ['name', 'price', 'created_at']

    def get_queryset(self):
        """
        Optionally restricts the returned products to a given category,
        by filtering against a 'category' query parameter in the URL.
        Example: /api/products/?category__name=Electronics
        """
        queryset = Product.objects.all()
        category_name = self.request.query_params.get('category', None)
        if category_name is not None:
            queryset = queryset.filter(category__name__iexact=category_name) # Case-insensitive match for category name
        return queryset.filter(is_available=True).order_by('name') # Ensure only available products are returned

    def create(self, request, *args, **kwargs):
        # Override create method to restrict product creation to staff users
        if not request.user.is_staff: # Check if the user is a staff member
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    # Custom view for listing products with search functionality
    # This view allows searching products by name or description.  
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter] # Ensure SearchFilter is included
    search_fields = ['name', 'description'] # Fields to search within
