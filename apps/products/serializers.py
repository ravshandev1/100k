from rest_framework import serializers
from .models import Product, Wishlist, Category, ProductRate, ProductImage, ProductVideo, Shop


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductRateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRate
        fields = ['name', 'rate', 'comment']


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['video']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'shop', 'rate', 'product_video', 'product_image', 'product_rate',
                  'more_information']

    product_image = ProductImagesSerializer(many=True, read_only=True)
    product_rate = ProductRateListSerializer(many=True, read_only=True)
    product_video = ProductVideoSerializer(many=True, read_only=True)
    rate = serializers.SerializerMethodField()
    shop = ShopSerializer(read_only=True)

    @staticmethod
    def get_rate(obj):
        rates_count = ProductRate.objects.filter(product=obj).all().count()
        rates = ProductRate.objects.filter(product=obj).all()
        rates_sum = sum([item.rate for item in rates])
        if rates_count:
            return rates_sum // rates_count
        else:
            return 0


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'product_image']

    product_image = ProductImagesSerializer(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products_count']

    products_count = serializers.SerializerMethodField()

    @staticmethod
    def get_products_count(obj):
        return Product.objects.filter(category=obj).count()


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product']

    id = serializers.IntegerField(read_only=True)


class ProductRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRate
        fields = ['name', 'product', 'rate', 'comment']


class ProductAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'shop', 'for_admin', 'product_image']

    product_image = ProductImagesSerializer(many=True, read_only=True)
    shop = ShopSerializer(read_only=True)
