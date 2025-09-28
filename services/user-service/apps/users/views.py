from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, UserProfile
from .serializers import (
    UserWithProfileSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer
)

class RegisterView(generics.CreateAPIView):
    """Представление для регистраций"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

class ProfileView(generics.RetrieveUpdateAPIView):
    """Представление для показа профиля юзеру, берет айди через рекуест и возвращает ему профиль юзера"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] # ТОлько для авторизованныъх

    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile