"""hotelmgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from account.views import HotelTokenObtainPairView, UserViewSet
from guest.views import GuestViewSet
from room.views import BookingViewSet, DiscountViewSet, MiniBarPaymentViewSet, PaymentViewSet, RoomViewSet

# swagger api document
schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Management API",
      default_version='v1',
      description="Hotel Management API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tsvetchik@gmail.com"),
      license=openapi.License(name="Hotel Management Lisence"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# api router 
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'minibar-payments', MiniBarPaymentViewSet)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', HotelTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('account.urls')),
    path('', include('room.urls')),
    path('', include(router.urls)),
    path("admin/", admin.site.urls),

]
