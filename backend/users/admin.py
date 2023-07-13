from django.contrib import admin

from .models import User


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


admin.site.register(User, UserAdmin)
