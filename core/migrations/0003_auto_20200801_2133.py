# Generated by Django 3.0.8 on 2020-08-02 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200801_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='items_total',
            new_name='total',
        ),
    ]
