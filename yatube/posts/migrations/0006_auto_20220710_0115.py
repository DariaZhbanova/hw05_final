# Generated by Django 2.2.16 on 2022-07-09 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20220630_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pics',
            field=models.ImageField(blank=True, null=True, upload_to='img_post/'),
        ),
        migrations.AddField(
            model_name='post',
            name='text_title',
            field=models.CharField(blank=True, help_text='Привлеките внимание читателей самым важным', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Группа, наиболее подходящая по смыслу поста', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Group', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Поделитесь с общественностью важными новостями', verbose_name='Текст поста'),
        ),
    ]