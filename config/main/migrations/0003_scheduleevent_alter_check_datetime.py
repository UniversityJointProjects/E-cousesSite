# Generated by Django 4.1.6 on 2023-02-14 13:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_ceo_id_firm_directors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=250)),
                ('date', models.DateTimeField(default=datetime.datetime(1, 1, 1, 1, 1), verbose_name='Date and time')),
                ('color', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Schedule event',
                'verbose_name_plural': 'Schedule event',
            },
        ),
        migrations.AlterField(
            model_name='check',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 1, 1), verbose_name='Date and time'),
        ),
    ]
