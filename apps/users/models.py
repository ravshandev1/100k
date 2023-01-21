from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
from .permissions import CustomPermissionsMixin
from .role import Role

phone_regex = RegexValidator(
    regex=r'^998[0-9]{9}$',
    message="Phone number must be entered in the format: '998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **kwargs):
        if not phone:
            raise TypeError('Username did not come')
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **kwargs):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(phone, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, CustomPermissionsMixin):
    name = models.CharField(max_length=212, null=True, blank=True)
    surname = models.CharField(max_length=212, null=True, blank=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_regex])
    role = models.ForeignKey(Role, models.SET_NULL, null=True, )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    province = models.CharField(max_length=212, null=True, blank=True)
    district_or_city = models.CharField(max_length=212, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.phone} {self.name}'


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
