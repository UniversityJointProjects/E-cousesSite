# Generated by Django 4.1.6 on 2023-02-12 12:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('author', models.CharField(max_length=50, verbose_name='Author')),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('anons', models.CharField(max_length=250, verbose_name='Anons')),
                ('full_text', models.TextField(verbose_name='Full text')),
                ('date', models.DateTimeField(verbose_name='Publication date')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='photo_files', verbose_name='Course image')),
                ('date', models.DateField(default=datetime.date(1, 1, 1), verbose_name='Date')),
                ('time_to_read', models.CharField(max_length=50, verbose_name='Time to read')),
                ('description', models.CharField(max_length=500, verbose_name='Description')),
                ('content', models.TextField(verbose_name='Content')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('age', models.IntegerField(verbose_name='Age')),
            ],
            options={
                'verbose_name': 'Director',
                'verbose_name_plural': 'Directors',
            },
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('capitalization', models.IntegerField(verbose_name='Capitalization')),
                ('directors', models.ManyToManyField(to='main.director')),
            ],
            options={
                'verbose_name': 'Firm',
                'verbose_name_plural': 'Firms',
            },
        ),
        migrations.CreateModel(
            name='ProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=150, verbose_name='Login')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('bio', models.CharField(max_length=300, verbose_name='Bio')),
                ('avatar', models.ImageField(upload_to='avatars', verbose_name='Avatar')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='ShopQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleanliness', models.IntegerField(verbose_name='Cleanliness')),
                ('staff_courtesy', models.IntegerField(verbose_name='Staff courtesy')),
                ('products_quality', models.IntegerField(verbose_name='Products quality')),
            ],
            options={
                'verbose_name': 'ShopQuality',
                'verbose_name_plural': 'ShopsQualities',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('employees_number', models.IntegerField(verbose_name='Employees number')),
                ('shop_quality_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.shopquality')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('cost', models.IntegerField(verbose_name='Cost')),
                ('firm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.firm')),
            ],
        ),
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_file', models.FileField(upload_to='courses_files')),
                ('file_name', models.CharField(max_length=100, verbose_name='File name')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
            options={
                'verbose_name': 'Course file',
                'verbose_name_plural': 'Course files',
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime(1, 1, 1, 1, 1), verbose_name='Date and time')),
                ('cost', models.IntegerField(verbose_name='Cost')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop')),
            ],
            options={
                'verbose_name': 'Check',
                'verbose_name_plural': 'Checks',
            },
        ),
    ]
