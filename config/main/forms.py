from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from .models import *
from django import forms


class ShopQualityForm(ModelForm):

    @staticmethod
    def clone(request):
        return ShopQualityForm(request)

    @staticmethod
    def clone_instance(ins):
        return ShopQualityForm(instance=ins)

    class Meta:
        model = ShopQuality
        fields = ['cleanliness', 'staff_courtesy', 'products_quality']
        widgets = {
            "cleanliness": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + ShopQuality.names[1].lower() + '...'}),
            "staff_courtesy": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + ShopQuality.names[2].lower() + '...'}),
            "products_quality": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + ShopQuality.names[3].lower() + '...' })
        }


class ShopForm(ModelForm):

    @staticmethod
    def clone(request):
        return ShopForm(request)

    @staticmethod
    def clone_instance(ins):
        return ShopForm(instance=ins)

    class Meta:
        model = Shop
        fields = ['name', 'employees_number', 'shop_quality_id']
        widgets = {
            "name": TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Shop.names[1].lower() + '...'}),
            "employees_number": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Shop.names[2].lower() + '...'}),
            "shop_quality_id": forms.Select(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Shop.names[3].lower() + '...' })
        }


class DirectorForm(ModelForm):

    @staticmethod
    def clone(request):
        return DirectorForm(request)

    @staticmethod
    def clone_instance(ins):
        return DirectorForm(instance=ins)

    class Meta:
        model = Director
        fields = ['name', 'age']
        widgets = {
            "name": TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Director.names[1].lower() + '...'}),
            "age": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Director.names[2].lower() + '...'})
        }


class FirmForm(ModelForm):

    @staticmethod
    def clone(request):
        return FirmForm(request)

    @staticmethod
    def clone_instance(ins):
        return FirmForm(instance=ins)

    class Meta:
        model = Firm
        fields = ['name', 'capitalization', 'directors']
        widgets = {
            "name": TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Firm.names[1].lower() + '...'}),
            "capitalization": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Firm.names[2].lower() + '...'}),
            "directors": forms.SelectMultiple(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Firm.names[3].lower() + '...'})
        }


class ProductForm(ModelForm):

    @staticmethod
    def clone(request):
        return ProductForm(request)

    @staticmethod
    def clone_instance(ins):
        return ProductForm(instance=ins)

    class Meta:
        model = Product
        fields = ['name', 'cost', 'firm_id']
        widgets = {
            "name": TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Product.names[1].lower() + '...'}),
            "cost": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Product.names[2].lower() + '...'}),
            "firm_id": forms.Select(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Product.names[3].lower() + '...'})
        }


class CheckForm(ModelForm):

    @staticmethod
    def clone(request):
        return CheckForm(request)

    @staticmethod
    def clone_instance(ins):
        return CheckForm(instance=ins)

    class Meta:
        model = Check
        fields = ['datetime', 'cost', 'product_id', 'shop_id']
        widgets = {
            "datetime": forms.DateTimeInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Check.names[1].lower() + '...'}),
            "cost": forms.NumberInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Check.names[2].lower() + '...'}),
            "product_id": forms.Select(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Check.names[3].lower() + '...'}),
            "shop_id": forms.Select(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter ' + Check.names[4].lower() + '...'})
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

        widgets = {
            "username": forms.TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter username...'}),
            "password1": forms.PasswordInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Enter password...'}),
            "password2": forms.PasswordInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Repeat the password...'}),
        }


class CreateAnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', "date", "author", 'text']

        widgets = {
            "title": forms.TextInput(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Введите заголовок...'}),
            "text": forms.Textarea(
                attrs={'class': 'common_form_input_field',
                       'placeholder': 'Введите текст...'}),
        }
