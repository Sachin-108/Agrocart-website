# Generated by Django 4.2.4 on 2023-10-11 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='total_price',
        ),
    ]