# Generated by Django 2.1.3 on 2019-01-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181204_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='observation',
            field=models.CharField(choices=[('ok', 'Ok'), ('not_ok', 'Not Ok')], max_length=100, null=True, verbose_name='Observation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('owner', 'Proprietário'), ('real_estate', 'Imobiliária')], default='owner', max_length=20, verbose_name='Qual o seu perfil?'),
        ),
    ]
