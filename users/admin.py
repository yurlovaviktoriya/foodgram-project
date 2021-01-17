from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'last_name',
        'first_name',
        'email',
    )
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
