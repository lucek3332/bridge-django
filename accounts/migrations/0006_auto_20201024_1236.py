# Generated by Django 3.1.2 on 2020-10-24 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201021_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-is_online', 'user')},
        ),
    ]
