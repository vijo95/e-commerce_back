# Generated by Django 3.0.8 on 2020-08-03 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_orderitem_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='coupon',
        ),
    ]
