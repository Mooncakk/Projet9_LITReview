from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):

    fields = ['username', 'password', 'date_joined', 'is_superuser', 'is_staff', 'is_active', ]
    list_display = ('username', 'date_joined', 'last_login')


admin.site.register(User, UserAdmin)
