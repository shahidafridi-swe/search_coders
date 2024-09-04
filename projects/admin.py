from django.contrib import admin

from .models import Project, Review

@admin.register(Project)
class AdminProject(admin.ModelAdmin):
    list_display = ['id','get_owner_name', 'title']

    def get_owner_name(self, obj):
        return obj.owner.first_name
    get_owner_name.short_description = 'Owner Name' 
    


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['id','get_reviewer_name', 'get_project_title']

    def get_reviewer_name(self, obj):
        return obj.reviewer.first_name
    get_reviewer_name.short_description = 'Reviewer Name' 
    
    def get_project_title(self, obj):
        return obj.project.title
    get_project_title.short_description = 'Project Title' 
    