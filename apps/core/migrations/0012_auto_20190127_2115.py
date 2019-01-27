# Generated by Django 2.1.3 on 2019-01-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190127_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='default_observation',
            field=models.TextField(null=True, verbose_name='Default Observation'),
        ),
        migrations.AlterField(
            model_name='report',
            name='observation',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Observation'),
        ),
        migrations.AlterField(
            model_name='report',
            name='state',
            field=models.CharField(choices=[('ok', 'Ok'), ('not_ok', 'Not Ok'), ('not_analyzed', 'Not Analyzed')], max_length=30, verbose_name='State'),
        ),
    ]
