# Generated by Django 2.1.3 on 2019-02-06 14:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20190206_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='iugu_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name='Iugu Credit Card Data'),
        ),
    ]
