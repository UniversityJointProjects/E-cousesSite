from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.introduce, name="introduce"),
    path('introduce', views.introduce, name="introduce"),
    path('announcements', views.announcements, name="announcements"),
    path('announcements_create', views.announcements_create, name="announcements_create"),
    path('timetable', views.timetable, name="timetable"),
    path('table_show/<int:tk>', views.table_view, name='table_show'),
    path('change_table/<int:url_table_id>/<int:entry_id>/<command>', views.change_table, name='change_table'),
    path('registration', views.registration, name='registration'),
    path('login_view', views.login_view, name='login_view'),
    path('profile', views.profile, name='profile'),
    # LOGOUT_REDIRECT_URL
    path('logout', include('django.contrib.auth.urls'), name='logout'),
    path('course/<int:course_id>', views.course_view, name='course'),
    path('course/course_change/<command>/<int:course_id>', views.course_change_view, name='course_change'),
    path('course/all_courses', views.all_courses_view, name='all_courses'),
    path('course_subscription/verification/<int:course_id>/<command>', views.course_subscription_verification, name='course_subscription_verification'),
    path('rich_text_editor', views.rich_text_editor, name='rich_text_editor'),
    path('course/save_progress', views.save_progress, name='save_progress')
]
