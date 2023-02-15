from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.introduce, name="introduce"),
    path('introduce', views.introduce, name="introduce"),
    path('table_show/<int:tk>', views.table_view, name='table_show'),
    path('change_table/<int:url_table_id>/<int:entry_id>/<command>', views.change_table, name='change_table'),
    path('registration', views.registration, name='registration'),
    path('login_view', views.login_view, name='login_view'),
    path('schedule/<int:month>/<int:year>', views.schedule, name='schedule'),
    path('schedule/create_event', views.create_event, name='create_event'),
    path('schedule/get_events', views.get_events, name='get_events'),
    path('schedule/delete_event', views.delete_event, name='delete_event'),
    # LOGOUT_REDIRECT_URL
    path('logout', include('django.contrib.auth.urls'), name='logout')
]
