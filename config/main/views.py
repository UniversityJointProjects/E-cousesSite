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
            template = "admin"
        # elif user.groups.filter(name='director').exists():
        #     template = "Director"
        # elif user.groups.filter(name='client').exists():
        #     template = "Client"
        elif user.groups.filter(name='student').exists():
            template = "student"
        elif user.groups.filter(name='author').exists():
            template = "author"
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
            ProfileInfo.objects.create(login=request.POST.get("username"), avatar="avatars/no_avatar.png")

            form.save()
            Group.objects.get(name="student").user_set.add(User.objects.last())
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
    users_table = []
    role = get_role(request.user)

    if not user.is_authenticated:
        return redirect('introduce')

    for row in ProfileInfo.objects.all():
        users_table.append(row.get_dict())

    model = ProfileInfo.objects.filter(login=user)[0]
    all_users = ProfileInfo.objects.all()

    subscribed_courses = model.course.all()
    created_courses = Course.objects.filter(author_id=user)

    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, request.FILES)
        form_without_avatar = ProfileInfoFormWithoutAvatar(request.POST)

        if form.is_valid():
            editing_model = ProfileInfo.objects.filter(login=user)[0]

            try:
                ProfileInfo(avatar=request.FILES['avatar'])
                for field in form._meta.fields:
                    setattr(editing_model, field, form.cleaned_data.get(field))
            except:
                for field in form_without_avatar._meta.fields:
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
                                                 'form': form,
                                                 'subscribed_courses': subscribed_courses,
                                                 'created_courses': created_courses,
                                                 'all_users': all_users,
                                                 'role': role,
                                                 'users_table': users_table,
                                                 'users_table_names': ProfileInfo.names})


def course_view(request, course_id):
    courses = Course.objects.all().filter(id=course_id)
    isSubscribed = False

    if len(courses):
        course = courses[0]
        profile = ProfileInfo.objects.filter(login=request.user.username)[0]

        if course in profile.course.all():
            isSubscribed = True
        else:
            isSubscribed = False

        course_files = CourseFile.objects.all().filter(course=course)
        return render(request, 'main/course.html', {'course': course, 'course_files': course_files,
                                                    'isSubscribed': isSubscribed})
    else:
        print('Error. There is no such course to be found.')
        return redirect('all_courses')


def course_change_view(request, command, course_id):
    course_form = CourseForm()

    error = ''
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('introduce')
        else:
            error = 'Вы ввели некорректные данные*'

    return render(request, 'main/course_change.html', {'course_form': course_form, 'error': error})


def all_courses_view(request):
    courses = Course.objects.all()
    return render(request, 'main/all_courses.html', {'courses': courses})


def rich_text_editor(request):
    return render(request, 'main/rich_text_editor.html')


def course_subscription_verification(request, course_id, command):
    user = request.user
    profile = ProfileInfo.objects.filter(login=user.username)[0]

    if command == 'unsubscribe':
        profile.course.remove(course_id)
    elif command == 'subscribe':
        profile.course.add(course_id)

    return redirect('course', course_id)
