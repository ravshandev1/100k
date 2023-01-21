from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers, exceptions
from .models import User, phone_regex
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'image', 'phone', 'province', 'district_or_city', 'address', 'role']

    phone = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(source='role.name', read_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password', 'password2']

    phone = serializers.CharField(validators=[phone_regex])
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        pas1 = attrs['password']
        pas2 = attrs['password2']
        phone = attrs['phone']
        if User.objects.filter(phone=phone):
            raise exceptions.AuthenticationFailed({'success': False, 'message': 'Telefon raqam oldin ruyxatga olingam'})
        if pas1 != pas2:
            raise exceptions.AuthenticationFailed({'success': False, 'message': 'Parollar bir biriga mos kelmadi'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password']

    phone = serializers.CharField(required=True, validators=[phone_regex])
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        tel = attrs['phone']
        pas = attrs['password']
        user = authenticate(phone=tel, password=pas)
        if not user:
            raise exceptions.AuthenticationFailed({'success': False, 'message': 'Telefon yoki parol xato'})
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    password2 = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        pas1 = attrs['password']
        pas2 = attrs['password2']
        if pas1 != pas2:
            raise exceptions.AuthenticationFailed({'message': 'Yangi kiritilgan parollar bir biriga mos kelmadi!'})
        return attrs


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'email']

    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)


class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'password2', 'uidb64', 'token']

    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        uidb64 = attrs['uidb64']
        token = attrs['token']
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(id=_id).first()
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise exceptions.AuthenticationFailed(
                {'success': False, 'message': 'Bu link muddati utgan qaytadan urinib kuring!'})
        if password != password2:
            raise serializers.ValidationError(
                {'success': False, 'message': 'Yangi kiritilgan parollar bir biriga mos kelmadi!'})
        user.set_password(password)
        user.save()
        return attrs
