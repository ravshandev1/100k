from django.core.validators import RegexValidator
from django.db import models
from products.models import Product
from users.models import User, Region, phone_regex

card_number = RegexValidator(
    regex=r'[0-9]{16}$',
    message="Card number must be entered in the format: '[XXXX] [XXXX] [XXXX] [XXXX]'. Up to 16 digits allowed."
)


class Order(models.Model):
    STATUS = (
        ('Yangi', 'Yangi'),
        ("Qayta qo'ng'iroq", "Qayta qo'ng'iroq"),
        ("Qabul qilindi", "Qabul qilindi"),
        ("Spam", "Spam"),
        ('Yetkazilmoqda', 'Yetkazilmoqda'),
        ('Yetkazib berildi', 'Yetkazib berildi'),
        ('Rad qilindi', 'Rad qilindi'),
    )
    status = models.CharField(max_length=212, choices=STATUS, default='Yangi')
    product = models.ForeignKey(Product, models.SET_NULL, null=True)
    name = models.CharField(max_length=212)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    address = models.ForeignKey(Region, models.SET_NULL, null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} {self.status}'


class Stream(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='stream', limit_choices_to={'role': 1})
    name = models.CharField(max_length=250)
    summa = models.IntegerField(default=0)
    product = models.ForeignKey(Product, models.CASCADE, 'stream')
    orders = models.ManyToManyField(Order, 'stream')
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name} {self.name}'


class Payment(models.Model):
    card_number = models.IntegerField(validators=[card_number])
    summa = models.IntegerField()

    def __str__(self):
        return self.card_number
