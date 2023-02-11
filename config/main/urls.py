from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.introduce, name="introduce"),
    path('introduce', views.introduce, name="introduce"),
    path('table_show/<int:tk>', views.table_view, name='table_show'),
    path('change_table/<int:url_table_id>/<int:entry_id>/<command>', views.change_table, name='change_table'),
    path('registration', views.registration, name='registration'),
    path('login_view', views.login_view, name='login_view'),
    # LOGOUT_REDIRECT_URL
    path('logout', include('django.contrib.auth.urls'), name='logout'),
    path('course/<int:course_id>', views.course_view, name='course'),
    path('course/course_change/<command>/<int:course_id>', views.course_change_view, name='course_change'),
    path('course/all_courses', views.all_courses_view, name='all_courses')
]
