from django.contrib import admin
from .models import LoginStudent, TeacherAdmin

@admin.register(LoginStudent)
class LoginStudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'emailid', 'dept', 'year')
    search_fields = ('username', 'emailid')

@admin.register(TeacherAdmin)
class TeacherAdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'emailid', 'usertype', 'dept')
    search_fields = ('username', 'emailid')
    list_filter = ('usertype', 'dept')
