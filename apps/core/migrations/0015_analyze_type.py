# Generated by Django 2.1.3 on 2019-01-28 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190127_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyze',
            name='type',
            field=models.FileField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('ground', 'Ground'), ('site', 'Site')], default='house', upload_to='', verbose_name='Type'),
        ),
    ]
