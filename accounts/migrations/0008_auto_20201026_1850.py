# Generated by Django 3.1.2 on 2020-10-26 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_chat_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chat_status',
            field=models.IntegerField(default=0),
        ),
    ]
