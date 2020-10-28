# Generated by Django 3.0.8 on 2020-08-02 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200802_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='core.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='core.Address'),
        ),
    ]
