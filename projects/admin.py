from django.contrib import admin

from .models import Project

@admin.register(Project)
class AdminProject(admin.ModelAdmin):
    list_display = ['id','get_owner_name', 'title']

    def get_owner_name(self, obj):
        return obj.owner.first_name
    get_owner_name.short_description = 'Owner Name' 
    