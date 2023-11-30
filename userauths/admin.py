from django.contrib import admin
from userauths.models import User


# Register your models here.
class Useradmin(admin.ModelAdmin):
    list_display = ['username','email','bio']
admin.site.register(User, Useradmin)