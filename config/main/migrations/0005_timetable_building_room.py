# Generated by Django 4.1.6 on 2023-02-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_timetable_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='building_room',
            field=models.TextField(default='3-306', verbose_name='Builing and room'),
            preserve_default=False,
        ),
    ]