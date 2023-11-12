from django.contrib import admin

from .models import Ticket, UserFollows, Review


# Register your models here.


class TicketAdmin(admin.ModelAdmin):

    title = 'Titre'
    list_display = ('title', 'description', 'user', 'time_created', 'last_update')
    list_filter = ['user']
    search_fields = ['title']


admin.site.register(Ticket, TicketAdmin)


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('ticket', 'headline', 'rating', 'user', 'time_created', 'last_update')
    list_filter = ['rating']
    search_fields = ['headline']


admin.site.register(Review, ReviewAdmin)


class UserFollowsAdmin(admin.ModelAdmin):

    list_display = ('user', 'followed_user')


admin.site.register(UserFollows, UserFollowsAdmin)
