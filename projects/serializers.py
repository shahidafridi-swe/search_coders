from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)  
    owner_id = serializers.IntegerField(source='owner.id', read_only=True) 


    class Meta:
        model = Project
        fields = ['id', 'owner','owner_id', 'owner_name', 'title', 'description', 'featured_image', 'demo_link', 'source_link', 'created_at']
        extra_kwargs = {
            'owner': {'write_only': True}  
        }
