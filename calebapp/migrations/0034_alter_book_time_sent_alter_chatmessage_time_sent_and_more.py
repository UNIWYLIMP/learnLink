# Generated by Django 4.1.1 on 2022-12-07 08:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calebapp', '0033_alter_book_time_sent_alter_chatmessage_time_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 327580)),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 311950)),
        ),
        migrations.AlterField(
            model_name='groupmessage',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 311950)),
        ),
        migrations.AlterField(
            model_name='news',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 327580)),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 327580)),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 9, 3, 17, 327580)),
        ),
    ]
