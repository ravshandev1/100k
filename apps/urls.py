from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('refresh/', TokenRefreshView.as_view()),
]
