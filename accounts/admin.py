from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin


@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    list_filter = list(AbstractUserAdmin.list_filter)
    list_filter.remove('is_active')
    list_filter = tuple(list_filter)

    list_display = list(AbstractUserAdmin.list_display)
    list_display.remove('first_name')
    list_display.remove('last_name')
    list_display = tuple(list_display)

    fieldsets = AbstractUserAdmin.fieldsets
    fieldsets[1][1]['fields'] = ('email',)
    fieldsets[2][1]['fields'] = list(fieldsets[2][1]['fields'])
    fieldsets[2][1]['fields'].remove('is_active')
    fieldsets = tuple(fieldsets)

    readonly_fields = ('last_login', 'date_joined')
