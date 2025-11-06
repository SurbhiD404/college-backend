from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UpdateUserSerializer
from rest_framework_simplejwt.exceptions import TokenError
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'msg': 'Welcome!', 'token': str(refresh.access_token)})
        return Response({'error': serializer.errors}, status=400)
    except Exception as e:
        return Response({'error': 'Fix: ' + str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user and user.email and '@' in user.email:
            refresh = RefreshToken.for_user(user)
            return Response({
                'msg': 'Login successful!',
                'refresh': str(refresh),           
                'access': str(refresh.access_token), 
                'user': user.username
            })
        return Response({'error': 'Wrong details or not college email!'}, status=401)
    except Exception as e:
        return Response({'error': 'Login failed: ' + str(e)}, status=400)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = request.user.profile
    if request.method == 'GET':
        return Response(ProfileSerializer(profile).data)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'Updated!'})
    return Response({'error': serializer.errors}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {"error": "refresh_token is required in body"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"msg": "Logged out successfully!"}, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Logout failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    serializer = UpdateUserSerializer(request.user, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Updated!", "user": {"username": request.user.username, "email": request.user.email}})
    return Response(serializer.errors, status=400)

