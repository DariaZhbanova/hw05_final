# Generated by Django 2.2.16 on 2022-07-17 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_auto_20220718_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Напишите Ваши впечатления после прочтения поста', max_length=200, null=True, verbose_name='Ваш комментарий'),
        ),
    ]