# Generated by Django 2.1.3 on 2019-01-27 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190127_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='observation',
            field=models.CharField(max_length=100, null=True, verbose_name='Observation'),
        ),
    ]
