# Generated by Django 5.0.6 on 2024-07-21 20:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='Date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
