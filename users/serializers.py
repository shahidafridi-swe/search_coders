from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import send_mail  
from django.urls import reverse 
from django.contrib.auth import authenticate

class ProfileSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(required=True)
    class Meta:
        model = Profile
        fields = ['domain', 'location', 'bio', 'profile_image', 
                  'social_github', 'social_twitter', 
                  'social_linkedin', 'social_youtube', 
                  'social_website']
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True,'allow_blank': False},
            'last_name': {'required': True,'allow_blank': False},
            'email': {'required': True, 'allow_blank': False} 
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  
        )
        Profile.objects.create(user=user, **profile_data)
        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activate_url = f"http://127.0.0.1:8000/{activation_link}"

        subject = 'Activate Your Account'
        message = f'Hi {user.username},\n\nPlease click the link below to activate your account:\n{activate_url}'
        from_email = 'noreply@searchCoders.com'
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data