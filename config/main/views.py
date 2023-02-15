from bs4 import BeautifulSoup
from django.contrib.auth.models import Group
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest, JsonResponse

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
            template = "none"
    return template


def get_ava(user):
    if user.is_authenticated:
        profiles_ava = ProfileInfo.objects.filter(name=user).get().avatar

        return profiles_ava
    else:
        return ""


# def index(request):
#     checks = Check.objects.all()
#     return render(request, "main/index.html", {'checks': checks})


def introduce(request):
    role = get_role(request.user)
    ava = get_ava(request.user)

    return render(request, "main/introduce.html", {'role': role, 'ava': ava})


def announcements(request):
    role = get_role(request.user)
    ava = get_ava(request.user)
    profiles = ProfileInfo.objects.all()
    data = Announcement.objects.all()
    new_data = []

    for item in data:
        new_data.append({"title": item.title, "author": item.author, "text": item.text, "date": item.date, "avatar_url": f"media/{profiles.filter(name=item.author).get().avatar}"})

    return render(request, "main/announcements.html", {'role': role, 'ava': ava, "announcements": new_data})


def announcements_create(request):
    role = get_role(request.user)
    ava = get_ava(request.user)
    form = CreateAnnouncementForm

    if request.method == "POST":
        caform = CreateAnnouncementForm({"title": request.POST["title"], "date": datetime.date.today(), "author": request.user, "text": request.POST["text"]})

        if caform.is_valid():
            caform.save()
            return redirect('announcements')

    return render(request, "main/announcements_create.html", {'role': role, 'ava': ava, "form": form})


def timetable(request):
    role = get_role(request.user)
    ava = get_ava(request.user)

    return render(request, "main/timetable.html", {'role': role, 'ava': ava})


def timetable_edit(request):
    role = get_role(request.user)
    ava = get_ava(request.user)
    form = TimetableForm

    if request.method == "POST":
        caform = TimetableForm(request.POST)

        if caform.is_valid():
            caform.save()
            return redirect('timetable')

    timetable_els = Timetable.objects.all()
    timetable_data = []

    for item in timetable_els:
        pass#print(f"{item.WEEKDAYS[item.weekday]}")

    return render(request, "main/timetable_edit.html", {'role': role, 'ava': ava, "form": form, "data": timetable_data})




def change_table(request, url_table_id, entry_id, command):
    forms = [ShopQualityForm, ShopForm, DirectorForm, FirmForm, ProductForm, CheckForm]
    existing_models = [ShopQuality, Shop, Director, Firm, Product, Check]
    form = forms[url_table_id]
    role = get_role(request.user)
    ava = get_ava(request.user)

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
        'role': role, 'ava': ava})


def table_view(request, tk):
    table = []
    existing_models = [ShopQuality, Shop, Director, Firm, Product, Check]
    current_model = existing_models[tk]
    role = get_role(request.user)
    ava = get_ava(request.user)

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
        'role': role, 'ava': ava})


def registration(request):
    form = CreateUserForm
    role = get_role(request.user)
    ava = get_ava(request.user)

    if request.user.is_authenticated:
        return redirect('introduce')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            ProfileInfo.objects.create(login=request.POST.get("username"), avatar="avatars/no_avatar.png")

            form.save()
            Group.objects.get(name="student").user_set.add(User.objects.last())
            return redirect('login_view')

    return render(request, 'main/registration.html', {'form': form, 'ava': ava, 'role': role})


def login_view(request):
    role = get_role(request.user)
    ava = get_ava(request.user)

    if request.user.is_authenticated:
        return redirect('introduce')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('introduce')
    return render(request, 'main/login.html', {'role': role, 'ava': ava})


def profile(request):
    user = request.user
    users_table = []
    role = get_role(request.user)
    ava = get_ava(request.user)

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
                                                 'role': role, 'ava': ava,
                                                 'users_table': users_table,
                                                 'users_table_names': ProfileInfo.names})


def replace_tag(html, replaced_tag, tag_replacement) -> str:
    return html.replace(
        f'<{replaced_tag}>', f'<{tag_replacement}>').replace(f'</{replaced_tag}>', f'</{tag_replacement}>')




def parse_passed0(html) -> str:
    html_new = html.replace(
        '<passed>',
        '<div class="pass_button"><a href="" class="passed">').replace(
        '</passed>',
        '</a></div>')
    return html_new

def parse_passed0(html, start, end) -> str:
    html_new = html.replace(
        '<passed>',
        '<div class="pass_button"><a href="" class="passed">').replace(
        '</passed>',
        '</a></div>')
    return html_new


def get_tag_content(tag_code) -> str:
    content_start = tag_code.find(">") + 1
    content_end = tag_code.find("</", content_start) - 1
    return tag_code[content_start:(content_end + 1)]


def parse_mark_as_passed(html, button_id) -> str:
    tag_opening = f'<div class="progress_button" button_id="{button_id}">'
    tag_content = get_tag_content(html)
    tag_closing = '</div>'
    return tag_opening + tag_content + tag_closing


def parse_passed(html, button_id) -> str:
    tag_opening = f'<div class="progress_button" button_id="{button_id}">'
    tag_content = get_tag_content(html)
    tag_closing = '</div>'
    return tag_opening + tag_content + tag_closing


def get_tag_attribute_value(html, tag, attribute):
    pass


def get_tag_range(html, tag, entry_number):
    start_tag = f'<{tag}'
    end_tag = f'</{tag}>'
    start = 0
    current_entry_number = 0
    while current_entry_number <= entry_number and start != -1:
        start = html.find(start_tag, start)
        current_entry_number += 1
        if current_entry_number <= entry_number and start != -1:
            start += 1
    end = html.find(end_tag, start) + len(end_tag) - 1
    if start >= end or start == -1 or end == -1:
        start = -1
        end = -1
    return [start, end]


def get_tag_attributes(html, tag, entry_number):
    tag_range = get_tag_range(html, tag, entry_number)
    sub_str = html[tag_range[0]:tag_range[1]]
    soup = BeautifulSoup(sub_str, 'html.parser')
    found = soup.find(tag)
    if found is not None:
        return found.attrs
    else:
        return {}


def parse_progress(html, user, course) -> str:
    tag_range = [0, 0]
    current_entry = 0
    while tag_range[0] != -1 and tag_range[1] != -1:
        tag_range = get_tag_range(html, "passed", 0)
        if user.id is None:
            html = html[0:tag_range[0]] + html[tag_range[1] + 1:]
        else:
            attributes = get_tag_attributes(html[tag_range[0]:tag_range[1] + 1], "passed", 0)
            if len(attributes) > 0:
                button_id = attributes["button_id"]
                progresses = CourseProgress.objects.filter(button_id=button_id, course=course, user=user)
                if len(progresses) <= 0:
                    progresses = [CourseProgress()]
                    setattr(progresses[0], "user", user)
                    setattr(progresses[0], "course", course)
                    setattr(progresses[0], "button_id", button_id)
                    setattr(progresses[0], "state", False)
                    progresses[0].save()

                progress_state = getattr(progresses[0], "state")

                if progress_state:
                    part = parse_passed(html[tag_range[0]:tag_range[1] + 1], button_id)
                else:
                    part = parse_mark_as_passed(html[tag_range[0]:tag_range[1] + 1], button_id)
                html = html[0:tag_range[0]] + part + html[tag_range[1] + 1:]
        current_entry += 1
    return html



def parse_html(html, user, course) -> str:
    # html_new = parse_mark_as_passed(html)
    # html_new = parse_passed(html_new)
    html_new = parse_progress(html, user, course)
    return html_new


def course_view(request, course_id):
    courses = Course.objects.all().filter(id=course_id)
    user = request.user
    isSubscribed = False

    role = get_role(request.user)
    ava = get_ava(request.user)
    
    if len(courses):
        course = courses[0]
        if user.is_authenticated:
            profile = ProfileInfo.objects.filter(login=request.user.username)[0]
            if course in profile.course.all():
                isSubscribed = True
            else:
                isSubscribed = False

        # attrs = get_tag_attributes('<passed class  ="kek" button_id =  "15"></passed> <passed class  ="kek" button_id =  "30"></passed>', "passed", 1)
        # print(attrs["button_id"])
        course_files = CourseFile.objects.all().filter(course=course)
        course.content = parse_html(course.content, user, course)

        return render(request, 'main/course.html', {'course': course, 'course_files': course_files, 'role': role,
                                                    'ava': ava, 'isSubscribed': isSubscribed})
    else:
        print('Error. There is no such course to be found.')
        return redirect('all_courses')


def course_change_view(request, command, course_id):
    course_form = CourseForm()
    role = get_role(request.user)
    ava = get_ava(request.user)

    error = ''
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if command == 'add':
            if form.is_valid():
                form.instance.author_id = request.user
                form.instance.date = datetime.datetime.now().date()
                form.save()
                return redirect('introduce')
            else:
                error = 'Вы ввели некорректные данные*'
        elif command == 'update':
            updated_course = Course.objects.filter(id=course_id)[0]
            if form.is_valid():
                for field in form._meta.fields:
                    if field != 'author_id' and field != 'date':
                        setattr(updated_course, field, form.cleaned_data.get(field))
                updated_course.save()
                return redirect('course', course_id)
            else:
                print('course_change_view. command = update. Form is not valid')
                redirect('all_courses_view')

    if command == 'update':
        updated_course = Course.objects.filter(id=course_id)[0]
        course_form = CourseForm(instance=updated_course)

    return render(request, 'main/course_change.html', {'course_form': course_form, 'error': error, 'role': role, 'ava': ava})


def all_courses_view(request):
    courses = Course.objects.all()
    role = get_role(request.user)
    ava = get_ava(request.user)

    return render(request, 'main/all_courses.html', {'courses': courses, 'user': request.user, 'role': role, 'ava': ava})


def rich_text_editor(request):
    return render(request, 'main/rich_text_editor.html')


def course_subscription_verification(request, course_id, command):
    user = request.user

    if not user.is_authenticated:
        return redirect('introduce')

    profile = ProfileInfo.objects.filter(login=user.username)[0]
    if command == 'unsubscribe':
        profile.course.remove(course_id)
    elif command == 'subscribe':
        print(course_id)
        profile.course.add(course_id)

    return redirect('course', course_id)


def save_progress(request):
    button_id = request.POST.get('button_id')
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')
    state = request.POST.get('state') == 'true'

    progresses = CourseProgress.objects.get(button_id=button_id, course=course_id, user=user_id)
    progresses.state = state
    progresses.save()
    # progresses = CourseProgress.objects.filter(button_id=button_id, course=course_id, user=user_id)
    return JsonResponse({})


def get_progress_state(request):
    button_id = request.POST.get('button_id')
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')

    progresses = CourseProgress.objects.filter(button_id=button_id, course=course_id, user=user_id)

    return JsonResponse({'state': progresses[0].state})


def switch_progress_state(request):
    button_id = request.POST.get('button_id')
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')

    progresses = CourseProgress.objects.get(button_id=button_id, course=course_id, user=user_id)
    progresses.state = not progresses.state
    state = progresses.state
    progresses.save()

    return JsonResponse({'state': state})