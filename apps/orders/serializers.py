from rest_framework import serializers
from .models import Order, Stream, Payment
from users.models import Region, District


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'status', 'created_at', 'note', 'address']

    address = serializers.CharField(source='address.name')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'product', 'name', 'phone', 'note', 'address', 'created_at']

    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    phone = serializers.CharField(max_length=15)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'district_set']

    district_set = DistrictSerializer(read_only=True, many=True)


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'product', 'name', 'phone', 'note', 'address', 'created_at']

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    phone = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True, source='product.name')
    note = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True, source='address.name')


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'user', 'name', 'summa', 'product']

    id = serializers.IntegerField(read_only=True)
    summa = serializers.IntegerField(read_only=True)


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'name', 'views', 'new', 'accepted', 'delivery', 'delivered', 'call_back', 'spam', 'rejected']

    new = serializers.SerializerMethodField()
    accepted = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    delivered = serializers.SerializerMethodField()
    call_back = serializers.SerializerMethodField()
    spam = serializers.SerializerMethodField()
    rejected = serializers.SerializerMethodField()

    @staticmethod
    def get_new(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Yangi':
                c += 1
        return c

    @staticmethod
    def get_accepted(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Qabul qilindi':
                c += 1
        return c

    @staticmethod
    def get_delivery(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Yetkazilmoqda':
                c += 1
        return c

    @staticmethod
    def get_delivered(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Yetkazib berildi':
                c += 1
        return c

    @staticmethod
    def get_call_back(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == "Qayta qo'ng'iroq":
                c += 1
        return c

    @staticmethod
    def get_spam(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Spam':
                c += 1
        return c

    @staticmethod
    def get_rejected(obj):
        c = 0
        for i in obj.orders.all():
            if i.status == 'Rad qilindi':
                c += 1
        return c


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'card_number', 'summa']

    id = serializers.IntegerField(read_only=True)
