import datetime as datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class ShopQuality(models.Model):
    cleanliness = models.IntegerField('Cleanliness')
    staff_courtesy = models.IntegerField('Staff courtesy')
    products_quality = models.IntegerField('Products quality')

    title = "Shops quality"
    names = ["Index", "Cleanliness", "Staff courtesy", "Products quality"]

    def test_method(self):
        pass

    def get_dict(self, ):
        return {'id': self.id, 0: self.cleanliness, 1: self.staff_courtesy, 2: self.products_quality}

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ShopQuality"
        verbose_name_plural = "ShopsQualities"


class Shop(models.Model):
    name = models.CharField('Name', max_length=50)
    employees_number = models.IntegerField('Employees number')
    shop_quality_id = models.OneToOneField(ShopQuality, on_delete=models.CASCADE) #models.ForeignKey(ShopQuality, on_delete=models.CASCADE)

    title = "Shops"
    names = ["Index", "Name", "Employees number", "Shop quality id"]

    # def get_one_to_one(self):
    #     return {'is_relationship': True, 'related_field_table_id': 0}

    def get_dict(self):
        return {'id': self.id, 0: self.name, 1: self.employees_number, 2: self.shop_quality_id}

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"


class Director(models.Model):
    name = models.CharField('Name', max_length=50)
    age = models.IntegerField('Age')

    title = "Directors"
    names = ["Index", "Name", "Age"]

    def get_dict(self):
        return {'id': self.id, 0: self.name, 1: self.age}

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"


class Firm(models.Model):
    name = models.CharField('Name', max_length=50)
    capitalization = models.IntegerField('Capitalization')
    directors = models.ManyToManyField(Director) #models.ForeignKey(Director, on_delete=models.CASCADE)

    title = "Firms"
    names = ["Index", "Name", "Capitalization", "Directors"]

    def get_dict(self):
        return {'id': self.id, 0: self.name, 1: self.capitalization, 2: ", ".join(map(str, self.directors.all()))}

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firm"
        verbose_name_plural = "Firms"


class Product(models.Model):
    name = models.CharField('Name', max_length=50)
    cost = models.IntegerField('Cost')
    firm_id = models.ForeignKey(Firm, on_delete=models.CASCADE)

    title = "Products"
    names = ["Index", "Name", "Cost", "Firm id"]

    def get_dict(self):
        return {'id': self.id, 0: self.name, 1: self.cost, 2: self.firm_id}

    def __str__(self):
        return str(self.id)


class Check(models.Model):
    datetime = models.DateTimeField('Date and time', default=datetime.datetime(1, 1, 1, 1, 1))
    cost = models.IntegerField('Cost')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    title = "Checks"
    names = ["Index", "Date and time", "Cost", "Shop id", "Product id"]

    def get_dict(self):
        return {'id': self.id, 0: self.datetime, 1: self.cost, 2: self.shop_id, 3: self.product_id}

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Check"
        verbose_name_plural = "Checks"


class Course(models.Model):

    title = models.CharField('Title', max_length=250)
    course_image = models.ImageField('Course image', upload_to="photo_files", null=True, blank=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('Date', default=datetime.date(1, 1, 1))
    time_to_read = models.CharField('Time to read', max_length=50)
    description = models.CharField('Description', max_length=500)
    # content = RichTextField(blank=True, null=True)
    content = models.TextField('Content')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_file = models.FileField(upload_to="courses_files")
    file_name = models.CharField('File name', max_length=100)

    def __str__(self):
        return str(self.file_name)

    class Meta:
        verbose_name = "Course file"
        verbose_name_plural = "Course files"


class Article(models.Model):
    title = models.CharField('Title', max_length=50)
    anons = models.CharField('Anons', max_length=250)
    full_text = models.TextField('Full text')
    date = models.DateTimeField('Publication date')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'




class Announcement(models.Model):
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    title = models.CharField("Title", max_length=50)
    date = models.DateField("Date")
    author = models.CharField("Author", max_length=50)
    text = models.TextField("Text")


class ProfileInfo(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    login = models.CharField("Login", max_length=150)
    name = models.CharField("Name", max_length=50)
    surname = models.CharField("Surname", max_length=50)
    city = models.CharField("City", max_length=50)
    email = models.EmailField("Email", max_length=50)
    bio = models.CharField("Bio", max_length=300)
    avatar = models.ImageField("Avatar", upload_to='avatars')

    def __str__(self):
        return self.login + " _"
