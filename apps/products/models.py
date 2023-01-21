from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=212)
    image = models.ImageField('categories')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField( upload_to='shops', null=True, blank=True)
    url = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    for_admin = models.IntegerField(null=True)
    category = models.ForeignKey(Category, models.SET_NULL, null=True)
    price = models.FloatField()
    shop = models.ForeignKey(Shop, models.SET_NULL, 'product', null=True, blank=True)
    more_information = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_images')


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_video')
    video = models.FileField()


class ProductRate(models.Model):
    RATE = (
        (1, 'Juda Yomon'),
        (2, 'Yomon'),
        (3, 'Qoniqarli'),
        (4, 'Yaxshi'),
        (5, 'Ajoyib'),
    )
    name = models.CharField(max_length=212)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_rate')
    rate = models.IntegerField(choices=RATE, default=1)
    comment = models.TextField()

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'wishlist')
    product = models.ForeignKey(Product, models.CASCADE, 'wishlist')

    class Meta:
        ordering = ['-id']
