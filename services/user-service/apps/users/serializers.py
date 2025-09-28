from rest_framework import serializers
from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор берет моедль Юзерс и вернет поля из фиелдс"""
    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name', 'username', 'is_active', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth']

class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta: 
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Для регистраций объявляем пасворд и пасворд конфирм, берем модель юзерс и вернет поля из филдс"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Password do not match.')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user