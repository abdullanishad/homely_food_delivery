# Generated by Django 3.0.8 on 2020-08-14 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200814_0201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
    ]
