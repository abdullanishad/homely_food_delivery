# Generated by Django 3.0.8 on 2020-08-13 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200813_2355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='total_item_price',
            new_name='total_orderitem_price',
        ),
    ]
