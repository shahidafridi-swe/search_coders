from rest_framework import serializers
from .models import Project, Review

# class ProjectSerializer(serializers.ModelSerializer):
#     owner_name = serializers.CharField(source='owner.first_name', read_only=True)  
#     owner_id = serializers.IntegerField(source='owner.id', read_only=True) 


#     class Meta:
#         model = Project
#         fields = ['id', 'owner','owner_id', 'owner_name', 'title', 'description', 'featured_image', 'demo_link', 'source_link', 'created_at']
#         extra_kwargs = {
#             'owner': {'write_only': True}  
#         }
        
class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()  
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'owner', 'owner_id', 'owner_name', 'title', 'description', 'featured_image', 'demo_link', 'source_link', 'created_at']
        extra_kwargs = {
            'owner': {'write_only': True},
            'featured_image': {'required': False, 'allow_null': True},  
        }

    # Method to return owner's full name
    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

      
class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_reviewer_name(self, obj):
        return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"