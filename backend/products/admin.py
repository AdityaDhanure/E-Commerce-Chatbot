from django.contrib import admin
from .models import Product, ProductCategory

# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description', 'sku')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'category', 'image_url', 'sku')
        }),
        ('Inventory & Availability', {
            'fields': ('stock_quantity', 'is_available')
        }),
    )
