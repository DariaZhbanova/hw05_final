# Generated by Django 2.2.16 on 2022-07-17 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pics',
            new_name='image',
        ),
    ]
