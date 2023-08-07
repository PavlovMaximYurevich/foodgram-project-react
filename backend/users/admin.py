from django import forms
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



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ('user', 'author')
        # readonly_fields = ('question_id',)

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        author = cleaned_data.get('author')
        # true_answer = cleaned_data.get("true_answer")
        if user == author:
            raise ValidationError("Нельзя Подписаться на себя")
        return cleaned_data


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
