# Generated by Django 2.1.3 on 2019-01-30 11:57

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20190129_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='credit',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=20, verbose_name='Credit available for new requests'),
        ),
        migrations.AlterField(
            model_name='account',
            name='credit_used',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=20, verbose_name='Credit used'),
        ),
        migrations.AlterField(
            model_name='account',
            name='requests',
            field=models.IntegerField(default=0, verbose_name='Requests available for free'),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
