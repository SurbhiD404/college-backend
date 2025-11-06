from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match!")
        if not data['email'].lower().endswith(('@akgec.ac.in', '@akgec.edu.in')):  
            raise serializers.ValidationError("Use college email only!")
        if len(data['password']) < 6:
            raise serializers.ValidationError("Password min 6 chars!")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)

    def validate_email(self, value):
        if not value.lower().endswith('@akgec.ac.in'):
            raise serializers.ValidationError("Use college email!")
        if User.objects.filter(email=value).exclude(pk=self.context['request'].user.pk).exists():
            raise serializers.ValidationError("Email taken!")
        return value

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'email' in validated_data:
            instance.email = validated_data['email']
        instance.save()
        return instance        