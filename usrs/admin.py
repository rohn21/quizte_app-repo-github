from django.contrib import admin
from usrs.models import User, Student
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", )
admin.site.register(User, UserAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "school_name", )
admin.site.register(Student, StudentAdmin)

# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ("designation",)    
# admin.site.register(Teacher)