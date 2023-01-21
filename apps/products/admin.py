from django.contrib import admin
from .models import Product, Category, ProductImage, ProductVideo, ProductRate, Shop, Wishlist


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


class ProductRateInline(admin.TabularInline):
    model = ProductRate
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVideoInline]
    list_display = ['id', 'name', 'category', 'price', 'rate']

    @staticmethod
    def rate(obj):
        rates = ProductRate.objects.filter(product=obj).all()
        rates_sum = sum([item.rate for item in rates])
        bs = ProductRate.objects.filter(product=obj).all().count()
        if bs:
            return rates_sum // bs
        else:
            return 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']

    @staticmethod
    def products_count(obj):
        return Product.objects.filter(category=obj).all().count()
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']