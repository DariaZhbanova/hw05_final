# Generated by Django 2.2.16 on 2022-07-17 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20220718_0037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text_comment',
            new_name='text',
        ),
    ]