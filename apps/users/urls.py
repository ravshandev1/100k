from django.urls import path
from .views import UserAPIView, UserLoginAPI, UserRegisterAPIView, ChangePasswordAPIView, ForgetPasswordAPIView, \
    SetPasswordAPIView

urlpatterns = [
    path('login/', UserLoginAPI.as_view()),
    path('<int:pk>/', UserAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('forget-password/', ForgetPasswordAPIView.as_view()),
    path('set-password/', SetPasswordAPIView.as_view()),
]
