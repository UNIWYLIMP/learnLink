# Generated by Django 4.1.1 on 2022-12-08 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calebapp', '0041_chatmessage_database_time_alter_book_time_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 6, 20, 16, 916867)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='database_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 8, 5, 20, 16, 916867, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='time_sent',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 12, 9, 5, 20, 16, 916867, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 6, 20, 16, 916867)),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 6, 20, 16, 916867)),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 6, 20, 16, 932494)),
        ),
    ]
