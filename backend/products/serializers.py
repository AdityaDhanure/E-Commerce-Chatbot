from rest_framework import serializers
from .models import ProductCategory, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__' # Include all fields from the model

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True) # Display category details
    # Allow setting category by ID, but don't require it
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source='category', write_only=True, required=False
    )
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_id',
            'stock_quantity', 'image_url', 'sku', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] # These fields are set by the backend