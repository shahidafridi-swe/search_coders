from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()  
    class Meta:
        model = Post
        fields = '__all__'
    
    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"