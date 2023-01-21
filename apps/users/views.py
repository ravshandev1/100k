from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, response, status, permissions, exceptions
from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, ChangePasswordSerializer, \
    SetPasswordSerializer, ForgetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import SendEmail


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return response.Response({'success': True}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['success'] = True
        return response.Response(data)


class UserRegisterAPIView(generics.CreateAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['success'] = True
        return response.Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPI(generics.GenericAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        data = {}
        refresh = RefreshToken.for_user(user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        data['user_data'] = UserSerializer(user).data
        data['success'] = True
        return response.Response(data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        tel = request.user.phone
        old_password = request.data['old_password']
        user = authenticate(phone=tel, password=old_password)
        if not user:
            raise exceptions.AuthenticationFailed({'message': 'Eski parol xato kiritildi!'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data['password']
        user.set_password(password)
        user.save()
        return response.Response({'message': 'Parol mofaqqiyatli uzgartirildi!'}, status=status.HTTP_200_OK)


class ForgetPasswordAPIView(generics.GenericAPIView):

    def get_serializer_class(self):
        return ForgetPasswordSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        user = User.objects.filter(phone=request.data['phone']).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            abs_url = f'{settings.CURRENT_SITE}/users/set-password/?uidb64={uidb64}&token={token}'
            email_body = f'Hello \n Use link below at reset password \n {abs_url}'
            data = {
                'to_email': request.data['email'],
                'email_subject': 'Reset password',
                'email_body': email_body
            }
            SendEmail.send_email(data)
            return response.Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
        return response.Response({'success': False, 'message': 'Username is not correct'},
                                 status=status.HTTP_400_BAD_REQUEST)


class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({'success': True, 'message': 'Successfully password changed!'})
