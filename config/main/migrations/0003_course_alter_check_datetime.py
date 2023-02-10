# Generated by Django 4.1.6 on 2023-02-10 14:26

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_ceo_id_firm_directors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date', models.DateTimeField(default=datetime.datetime(1, 1, 1, 1, 1), verbose_name='Date and time')),
                ('time_to_read', models.CharField(max_length=50, verbose_name='Time to read')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.AlterField(
            model_name='check',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 1, 1), verbose_name='Date and time'),
        ),
    ]
