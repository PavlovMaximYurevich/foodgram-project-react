from django.contrib import admin
from django.core.exceptions import ValidationError

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

    def validate(self, data):
        if data.get('user') == data.get('author'):
            raise ValidationError(
                'Нельзя подписаться на себя!'
            )
        return data


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
