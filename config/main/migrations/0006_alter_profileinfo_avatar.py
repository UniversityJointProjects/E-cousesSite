# Generated by Django 4.1.6 on 2023-02-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profileinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileinfo',
            name='avatar',
            field=models.ImageField(upload_to='photo_files', verbose_name='Avatar'),
        ),
    ]
