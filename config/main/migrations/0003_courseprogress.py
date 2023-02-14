# Generated by Django 4.1.6 on 2023-02-14 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_course_author_id_alter_course_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_id', models.IntegerField(verbose_name='Button id')),
                ('state', models.BooleanField(default=False, verbose_name='State')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прогресс курса',
                'verbose_name_plural': 'Прогрессы курсов',
            },
        ),
    ]