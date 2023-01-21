from django.urls import path
from .views import OrderCreateAPIView, OrderListAPIView, RegionAPIView, ChangeOrderStatus, StreamAPIView, StreamURLAPIView, StatisticsAPIView

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view()),
    path('list/', OrderListAPIView.as_view()),
    path('regions/', RegionAPIView.as_view()),
    path('status/<int:pk>/', ChangeOrderStatus.as_view()),
    path('stream/', StreamAPIView.as_view()),
    path('stream/<int:pk>/', StreamURLAPIView.as_view()),
    path('statistics/', StatisticsAPIView.as_view()),
]
