# Generated by Django 2.1.3 on 2019-01-27 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190127_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='indicator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Indicator', verbose_name='Indicator'),
        ),
    ]
