from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Request, Friend


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('username', 'id')
    list_filter = ('username', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('username',
                    'is_active', 'is_staff', 'id', )
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Request)
admin.site.register(Friend)
