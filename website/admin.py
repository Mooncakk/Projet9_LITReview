from django.contrib import admin

from .models import Ticket, UserFollows


# Register your models here.


class TicketAdmin(admin.ModelAdmin):

    list_display = ('title', 'description', 'user', 'time_created', 'last_update')
    list_filter = ['user']
    search_fields = ['title']


admin.site.register(Ticket, TicketAdmin)


class UserFollowsAdmin(admin.ModelAdmin):

    list_display = ('followed_user', )


admin.site.register(UserFollows, UserFollowsAdmin)
