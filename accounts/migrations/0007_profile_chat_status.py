# Generated by Django 3.1.2 on 2020-10-26 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201024_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chat_status',
            field=models.BooleanField(default=False),
        ),
    ]