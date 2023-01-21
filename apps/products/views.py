from rest_framework import generics, permissions, response, status
from .models import Product, Wishlist, Category, ProductRate
from .serializers import CategorySerializer, ProductSerializer, WishlistSerializer, ProductRateListSerializer, \
    ProductListSerializer, ProductAdminSerializer
from django.db.models import Q
from orders.models import Stream
from users.permissions import IsAuthenticatedAndIsAdmin


class CategoryAPIView(generics.ListAPIView):
    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('cat')
        q_condition = Q()
        if q:
            q_condition = Q(category__name__iexact=q)
        return qs.filter(q_condition)

    def get_serializer_class(self):
        return ProductListSerializer


class ProductRetrieveAPI(generics.RetrieveAPIView):

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        stream_id = self.request.query_params.get('stream')
        if stream_id:
            user = Stream.objects.filter(id=stream_id).first().user.phone
            stream = Stream.objects.filter(id=stream_id).first()
            stream.views += 1
            stream.save()
            qs = Stream.objects.filter(user__phone=user).all()
            query = []
            for i in qs:
                instance = Product.objects.filter(id=i.product.id).first()
                query.append(instance)
            data = serializer.data
            data['sotuvchining_boshqa_mahsulotlari'] = ProductListSerializer(query, many=True).data
            return response.Response(data)
        data = serializer.data
        return response.Response(data)


class ProductRateAPI(generics.CreateAPIView):
    def get_queryset(self):
        return ProductRate.objects.all()

    def get_serializer_class(self):
        return ProductRateListSerializer


class WishlistAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return WishlistSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        pid = request.data['product']
        product = Product.objects.get(id=pid)
        wlc = Wishlist.objects.filter(user=user, product=product).count()
        if wlc < 1:
            Wishlist.objects.create(user=user, product=product)
            data = {
                'success': True,
                'product': product.name,
                'message': 'Mahsulot muvaffaqiyatli sevimlilaringizga qushildi!'
            }
            return response.Response(data, status=status.HTTP_201_CREATED)
        else:
            Wishlist.objects.get(user=user, product=product).delete()
            data = {
                'success': False,
                'product': product.name,
                'message': 'Mahsulot muvaffaqiyatli sevimlilaringizga olindi!'
            }
            return response.Response(data, status=status.HTTP_200_OK)


class MyWishlistAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def get_queryset(self):
        user = self.request.user
        wish = Wishlist.objects.filter(user=user).all()
        qs = []
        for i in wish:
            qs.append(Product.objects.filter(name=i.product.name).first())
        return qs

    def get_serializer_class(self):
        return ProductListSerializer

    # @staticmethod
    # def get(request, *args, **kwargs):
    #     data = {}
    #     res = []
    #     user = request.user
    #     wishlists = Wishlist.objects.filter(user=user)
    #     products = []
    #     for i in wishlists:
    #         # products.append(i.product)
    #         data['id'] = i.product.id
    #         data['name'] = i.product.name
    #         data['image'] = ProductImagesSerializer(instance=i.product.product_image.all().first()).data
    #         data['price'] = i.product.price
    #     #     data = ProductListSerializer(instance=i.product).data
    #         res.append(data)
    #     # res.append(ProductListSerializer(instance=products, many=True).data)
    #     return response.Response(res, status=status.HTTP_200_OK)


class PopularAPI(generics.ListAPIView):
    def get_queryset(self):
        qs = Product.objects.filter(product_rate__rate__gte=1).all()[:8]
        if qs:
            return qs
        return Product.objects.all()[:8]

    def get_serializer_class(self):
        return ProductListSerializer


class ProductAdminAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedAndIsAdmin]

    def get_queryset(self):
        qs = Product.objects.all()
        q = self.request.query_params.get('cat')
        q_condition = Q()
        if q:
            q_condition = Q(category__name__iexact=q)
        return qs.filter(q_condition)

    def get_serializer_class(self):
        return ProductAdminSerializer
