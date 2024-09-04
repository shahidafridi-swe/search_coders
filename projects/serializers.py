from rest_framework import serializers
from .models import Project, Review

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.first_name', read_only=True)  
    owner_id = serializers.IntegerField(source='owner.id', read_only=True) 


    class Meta:
        model = Project
        fields = ['id', 'owner','owner_id', 'owner_name', 'title', 'description', 'featured_image', 'demo_link', 'source_link', 'created_at']
        extra_kwargs = {
            'owner': {'write_only': True}  
        }
        
        
class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"