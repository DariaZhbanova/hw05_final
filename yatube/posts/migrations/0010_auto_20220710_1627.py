# Generated by Django 2.2.16 on 2022-07-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20220710_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pics',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
