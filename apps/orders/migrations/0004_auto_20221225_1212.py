# Generated by Django 3.2.16 on 2022-12-25 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Yangi', 'Yangi'), ("Qayta qo'ng'iroq", "Qayta qo'ng'iroq"), ('Spam', 'Spam'), ('Yetkazilmoqda', 'Yetkazilmoqda'), ('Yetkazib berildi', 'Yetkazib berildi'), ('Rad qilindi', 'Rad qilindi')], default='Yangi', max_length=212),
        ),
    ]
