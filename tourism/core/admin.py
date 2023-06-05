"""django admin customizations"""


from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput
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
    list_display = ['title', 'user', ]
    readonly_fields = ['created_at', 'updated_at']

    # def get_author(self, obj):
    #     return obj.reservation.HotelAndResidence
    # 'HotelAndResidence__name'


class HotelAndResidenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'reservation', ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'star':
            # Override the default widget with a TextInput and
            # add some custom JavaScript to enforce the limit
            kwargs['widget'] = TextInput(attrs={
                'type': 'number',
                'min': 1,
                'max': 5,
                'oninput': 'if(value > 5) value = 5; if(value < 1) value = 1;',
            })
        return super().formfield_for_dbfield(db_field, request, **kwargs)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Reservation, ReservationAdmin)
admin.site.register(models.Comment)
admin.site.register(models.HotelAndResidence, HotelAndResidenceAdmin)
admin.site.register(models.TouristTour)
admin.site.register(models.TravelAgency)
