# Generated by Django 3.2.16 on 2022-12-16 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calebapp', '0044_auto_20221216_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 10, 30, 44, 33973)),
        ),
        migrations.AlterField(
            model_name='news',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 10, 30, 44, 36764)),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 10, 30, 44, 34808)),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 10, 30, 44, 54280)),
        ),
    ]
