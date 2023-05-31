"""django admin customizations"""


from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users """
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'address',
                    'phone_number', 'created_at', 'card_info', 'image']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
        (_('Contacts'), {'fields': ('phone_number', 'address', 'image')})
    )
    readonly_fields = ['last_login', 'created_at']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
                'address',
                'phone_number',
                'image'
            )
        }),
    )


class ReservationAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_filter = ('id', 'created_at', 'type')
    list_display = ['title', 'user']
    readonly_fields = ['user', 'created_at', 'updated_at']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Reservation, ReservationAdmin)
