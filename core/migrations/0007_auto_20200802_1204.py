# Generated by Django 3.0.8 on 2020-08-02 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200801_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='creation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='deletion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
