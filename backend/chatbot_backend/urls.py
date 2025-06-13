from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView as DefaultTokenObtainPairView

from chatbot_backend.serializers import MyTokenObtainPairSerializer # Import your custom serializer
from products.views import ProductViewSet, ProductCategoryViewSet


# Create a custom view class that explicitly uses your serializer
class CustomTokenObtainPairView(DefaultTokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer # Use your custom serializer for JWT token generation

from chat.views import ChatSessionViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'chat/sessions', ChatSessionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),     # Admin interface
    path('api/', include(router.urls)),       # Products and chat session APIs
    path('api/', include('accounts.urls')),        # User registration API
    path('api-auth/', include('rest_framework.urls')),   # DRF authentication endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),   # Custom token obtain view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # Token refresh view
]
