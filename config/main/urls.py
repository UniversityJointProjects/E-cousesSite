from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.introduce, name="introduce"),
    path('introduce', views.introduce, name="introduce"),
    path('announcements', views.announcements, name="announcements"),
    path('table_show/<int:tk>', views.table_view, name='table_show'),
    path('change_table/<int:url_table_id>/<int:entry_id>/<command>', views.change_table, name='change_table'),
    path('registration', views.registration, name='registration'),
    path('login_view', views.login_view, name='login_view'),
    path('profile', views.profile, name='profile'),
    # LOGOUT_REDIRECT_URL
    path('logout', include('django.contrib.auth.urls'), name='logout')
]
