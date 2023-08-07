from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
    )

    search_fields = ('username', 'email')
    list_filter = ('role',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('author', )


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
