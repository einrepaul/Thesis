from django.contrib import admin

from RHU.models import Account, Profile, Action

class AccountAdmin(admin.ModelAdmin):
    fields = ['role', 'profile', 'user']
    list_display = ('role', 'profile')

admin.site.register(Account, AccountAdmin)

class ProfileAdmin(admin.ModelAdmin):
    fields = [
        'firstname',
        'lastname',
        'sex',
        'birthday',
        'phone'
    ]

    list_display = ('firstname', 'lastname', 'birthday', 'created')

admin.site.register(Profile, ProfileAdmin)

class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ('timePerformed',)
    fields = [
        'type',
        'description',
        'user',
    ]
    list_display = ['user', 'type', 'description', 'timePerformed']
    list_filter = ('user', 'type', 'timePerformed')
    ordering = ('-timePerformed',)

admin.site.register(Action, ActionAdmin)