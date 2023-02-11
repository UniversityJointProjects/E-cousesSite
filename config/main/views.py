from django.contrib.auth.models import Group
from django.core.files.storage import default_storage

from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

locked_tables = [2, 3, 5]


def get_role(user):
    template = ""
    if user.is_authenticated:
        if user.is_superuser:
            template = "Director"
        elif user.groups.filter(name='director').exists():
            template = "Director"
        elif user.groups.filter(name='client').exists():
            template = "Client"
        else:
            template = "None"
    return template


# def index(request):
#     checks = Check.objects.all()
#     return render(request, "main/index.html", {'checks': checks})


def introduce(request):
    role = get_role(request.user)
    return render(request, "main/introduce.html", {'role': role})


def announcements(request):
    role = get_role(request.user)
    data = reversed(Announcement.objects.all())

    return render(request, "main/announcements.html", {'role': role, "announcements": data})


def change_table(request, url_table_id, entry_id, command):
    forms = [ShopQualityForm, ShopForm, DirectorForm, FirmForm, ProductForm, CheckForm]
    existing_models = [ShopQuality, Shop, Director, Firm, Product, Check]
    form = forms[url_table_id]
    role = get_role(request.user)

    if url_table_id in locked_tables and (role != "Director"):
        return redirect('/introduce')

    error = ''
    if request.method == "POST":
        form = forms[url_table_id].clone(request.POST)
        if form.is_valid():
            if command == 'add':
                form.save()
            elif command == 'edit':
                editing_model = existing_models[url_table_id].objects.filter(id=entry_id)[0]
                for field in form._meta.fields:
                    setattr(editing_model, field, form.cleaned_data.get(field))
                editing_model.save()
            return redirect('table_show', url_table_id)
        else:
            error = 'You entered incorrect data*'

    if command == 'edit':
        form = forms[url_table_id].clone_instance(existing_models[url_table_id].objects.filter(id=entry_id)[0])

    if command == 'delete':
        existing_models[url_table_id].objects.filter(id=entry_id).delete()
        return redirect('table_show', url_table_id)

    return render(request, "main/table_change.html", {
        'form': form,
        'names': existing_models[url_table_id].names,
        'error': error,
        'role': role})


def table_view(request, tk):
    table = []
    existing_models = [ShopQuality, Shop, Director, Firm, Product, Check]
    current_model = existing_models[tk]
    role = get_role(request.user)

    if tk in locked_tables and (role != "Director"):
        return redirect('/introduce')

    for row in current_model.objects.all():
        table.append(row.get_dict())

    return render(request, "main/index.html", {
        'names': current_model.names,
        'table': table,
        'table_id': tk,
        'title': current_model.title,
        'user': request.user,
        'role': role})


def registration(request):
    form = CreateUserForm
    role = get_role(request.user)
    if request.user.is_authenticated:
        return redirect('introduce')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_info_form = ProfileInfoForm({"login": request.POST.get("username"), "name": "",
                                              "surname": "", "city": "", "email": "", "bio": "", "avatar": ""})
            user_info_form.save()

            form.save()
            Group.objects.get(name="client").user_set.add(User.objects.last())
            return redirect('login_view')

    return render(request, 'main/registration.html', {'form': form, 'role': role})


def login_view(request):
    role = get_role(request.user)

    if request.user.is_authenticated:
        return redirect('introduce')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('introduce')
    return render(request, 'main/login.html', {'role': role})


def profile(request):
    user = request.user
    model = ProfileInfo.objects.filter(login=user)[0]

    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, request.FILES)

        # form = ProfileInfoForm.clone({"name": request.POST["name"], "surname": request.POST["surname"],
        #                              "city": request.POST["city"], "email": request.POST["email"],
        #                              "bio": request.POST["bio"],  "avatar": request.POST["avatar"]})
        if form.is_valid():
            editing_model = ProfileInfo.objects.filter(login=user)[0]
            print(str(editing_model))
            print("YEP")
            # setattr(editing_model, editing_model.name, form['name'].value())
            # setattr(editing_model, editing_model.surname, form['surname'].value())
            # setattr(editing_model, editing_model.city, form['city'].value())
            # setattr(editing_model, editing_model.email, form['email'].value())
            # setattr(editing_model, editing_model.bio, form['bio'].value())
            # if request.FILES:
            #    setattr(editing_model, editing_model.avatar, form['avatar'].value())

            # TODO добавить проверку на загрузку фотки

            for field in form._meta.fields:
                setattr(editing_model, field, form.cleaned_data.get(field))
            editing_model.save()
            return redirect('/profile')
    else:
        form = ProfileInfoForm()

    return render(request, 'main/profile.html', {'name': model.name,
                                                 'surname': model.surname,
                                                 'city': model.city,
                                                 'email': model.email,
                                                 'bio': model.bio,
                                                 'avatar': model.avatar,
                                                 'form': form})
