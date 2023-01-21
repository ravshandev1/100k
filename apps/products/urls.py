from django.urls import path
from .views import ProductListAPI, CategoryAPIView, ProductRetrieveAPI, ProductRateAPI, WishlistAPIView, \
    MyWishlistAPIView, PopularAPI, ProductAdminAPIView

urlpatterns = [
    path('', ProductListAPI.as_view()),
    path('<int:pk>/', ProductRetrieveAPI.as_view()),
    path('wishlist/', WishlistAPIView.as_view()),
    path('my-wishlist/', MyWishlistAPIView.as_view()),
    path('category/', CategoryAPIView.as_view()),
    path('rate/', ProductRateAPI.as_view()),
    path('ommabop/', PopularAPI.as_view()),
    path('admin/', ProductAdminAPIView.as_view()),
]
