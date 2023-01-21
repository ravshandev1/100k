from rest_framework import generics, response, permissions, status
from .serializers import OrderSerializer, CitySerializer, OrderRetrieveSerializer, StreamSerializer, PaymentSerializer, \
    StatisticsSerializer, OrderListSerializer
from .models import Order, Stream, Payment
from users.models import Region
from users.permissions import IsAuthenticatedAndIsAdmin
from django.conf import settings
from products.models import Product
from products.serializers import ProductListSerializer


class OrderCreateAPIView(generics.CreateAPIView):

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        stream_id = self.request.query_params.get('stream')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        if stream_id:
            obj = Stream.objects.filter(id=stream_id).first()
            obj.orders.add(serializer.data['id'])
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(phone=request.user.phone).all())
        products = []
        for i in queryset:
            products.append(i.product)
        serializer = self.get_serializer(products, many=True)
        data = []
        for (i, j) in zip(serializer.data, queryset):
            srd = OrderListSerializer(instance=j).data
            srd['image'] = i['product_image'][0]['image']
            srd['price'] = i['price']
            srd['product_name'] = i['name']
            data.append(srd)
        return response.Response(data)


class RegionAPIView(generics.ListAPIView):
    def get_queryset(self):
        return Region.objects.all()

    def get_serializer_class(self):
        return CitySerializer


class ChangeOrderStatus(generics.GenericAPIView):
    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return OrderRetrieveSerializer

    def patch(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        stat = serializer.data['status']
        if stat == 'Yetkazib berildi':
            if instance.stream:
                instance.stream.summa += instance.stream.product.for_admin
                instance.stream.save()
        return response.Response(serializer.data)


class PaymentAPIView(generics.CreateAPIView):
    def get_queryset(self):
        return Payment.objects.all()

    def get_serializer_class(self):
        return PaymentSerializer


class StreamAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedAndIsAdmin]
    queryset = Stream.objects.all()

    def get_serializer_class(self):
        return StreamSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user__phone=self.request.user.phone).all())
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for i in serializer.data:
            product = Product.objects.filter(id=i['product']).first()
            data.append({'id': i['id'], 'product': product.name, 'name': i['name'],
                         'stream_url': f"{settings.CURRENT_SITE}/orders/stream/{i['id']}/"})
        return response.Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StreamURLAPIView(generics.GenericAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def get(self, request, *args, **kwargs):
        stream = self.get_object()
        product = stream.product.id
        return response.Response({'url': f"{settings.CURRENT_SITE}/products/{product}?stream={stream.id}"})


class StatisticsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedAndIsAdmin]

    def get_serializer_class(self):
        return StatisticsSerializer

    def get_queryset(self):
        return Stream.objects.all()

    def get(self, request, *args, **kwargs):
        streams = self.get_queryset().filter(user=self.request.user).all()
        serializer = self.get_serializer(streams, many=True)
        return response.Response(serializer.data)
