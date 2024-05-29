# Generated by Django 4.1.1 on 2022-09-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calebapp', '0007_remove_peer_friend_list_peer_friend_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peer',
            name='friend_list',
        ),
        migrations.AddField(
            model_name='profile',
            name='friend_list',
            field=models.ManyToManyField(default=1, related_name='student_list', to='calebapp.peer'),
        ),
    ]
