from django.contrib import admin
from .models import Article, Shop, ShopQuality, Check, Director, Firm, Product, Announcement, ProfileInfo, Course, CourseFile, Timetable, CourseProgress, ScheduleEvent

admin.site.register(Article)
admin.site.register(Shop)
admin.site.register(ShopQuality)
admin.site.register(Check)
admin.site.register(Director)
admin.site.register(Firm)
admin.site.register(Product)
admin.site.register(ScheduleEvent)
admin.site.register(Announcement)

admin.site.register(ProfileInfo)
admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(CourseProgress)

admin.site.register(Timetable)
