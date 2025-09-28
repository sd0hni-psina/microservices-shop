from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from apps.users.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Proverka napisal li chtot-to user
    if not email or not password:
        return Response ({
            'error': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=email, password=password)
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response ({
                'error': 'Refresh token is required'
            },status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token)
        })
    except Exception as e:
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)