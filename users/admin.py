from django.contrib import admin

from .models import Profile, Skill

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'get_first_name', 'get_last_name', 'get_email']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Skill)
class AdminSkill(admin.ModelAdmin):
    list_display = ['name']
