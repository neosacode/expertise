# Generated by Django 2.1.3 on 2019-01-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_analyze_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyze',
            name='complement',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='complement'),
        ),
        migrations.AlterField(
            model_name='analyze',
            name='type',
            field=models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('ground', 'Ground'), ('site', 'Site')], default='house', max_length=30, verbose_name='Type'),
        ),
    ]
