# Generated by Django 3.0.8 on 2020-08-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
    ]
