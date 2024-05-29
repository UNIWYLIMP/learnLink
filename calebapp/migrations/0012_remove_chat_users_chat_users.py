# Generated by Django 4.1.1 on 2022-10-07 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calebapp', '0011_alter_peer_friend_list_alter_registration_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='users',
        ),
        migrations.AddField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(default=[0], related_name='chat_user_list', to='calebapp.profile'),
        ),
    ]
