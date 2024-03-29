# Generated by Django 2.1.3 on 2019-02-06 19:46

from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20190206_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=10, verbose_name='Valor')),
                ('ref', models.CharField(max_length=300, verbose_name='Valor')),
                ('state', models.CharField(default='created', max_length=30)),
            ],
            options={
                'verbose_name': 'Cobrança',
                'verbose_name_plural': 'Cobranças',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='document',
            field=models.CharField(max_length=20, null=True, verbose_name='CPF ou CNPJ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('owner', 'Pessoa Física'), ('real_estate', 'Imobiliária')], default='owner', max_length=20, verbose_name='Qual o seu perfil?'),
        ),
    ]
