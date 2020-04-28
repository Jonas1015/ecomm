# Generated by Django 3.0.4 on 2020-04-17 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0002_auto_20200417_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 17, 17, 54, 33, 933392)),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='items', to='ecomm_app.OrderItem'),
        ),
    ]