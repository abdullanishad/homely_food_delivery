# Generated by Django 3.0.8 on 2020-08-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200803_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(null=True),
        ),
    ]
