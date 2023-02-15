from django.contrib.auth.models import Group

from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, JsonResponse
import json

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


def schedule(request, month, year):
    return render(request, 'main/schedule.html', {'month': month, 'year': year})


def create_event(request):
    events = ScheduleEvent.objects.filter(day=int(request.POST.get('select_day')),
                                          month=int(request.POST.get('select_month')),
                                          year=int(request.POST.get('select_year')))

    model = ScheduleEvent()
    if len(events) > 0:
        model = events[0]

    model.event_name = request.POST.get('name')

    model.year = int(request.POST.get('select_year'))
    model.month = int(request.POST.get('select_month'))
    model.day = int(request.POST.get('select_day'))
    model.hour = int(request.POST.get('select_hour'))
    model.minute = int(request.POST.get('select_minute'))

    model.color = request.POST.get('color')
    model.description = request.POST.get('description')

    model.save()

    return JsonResponse({'test': 'test'})


def get_events(request):
    month = request.POST.get('month')
    year = request.POST.get('year')

    events = ScheduleEvent.objects.filter(month=month, year=year)
    data_str = ""

    for idx, e in enumerate(events):
        if idx > 0:
            data_str += '\n'
        data_str += f'{e.event_name}, {e.minute}, {e.hour}, {e.day}, {e.month}, {e.year}, {e.color}, {e.description}'

    print(f"{month} {year}")

    return JsonResponse({'count_events': len(events), 'data': data_str})


def delete_event(request):
    events = ScheduleEvent.objects.filter(day=int(request.POST.get('day')),
                                          month=int(request.POST.get('month')),
                                          year=int(request.POST.get('year')))
    if len(events) > 0:
        events[0].delete()
    return JsonResponse({})