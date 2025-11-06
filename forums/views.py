from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def list_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return Response(PostSerializer(posts, many=True).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_post(request):
    try:
        data = request.data.copy()
        data['anonymous'] = True
        if request.user.is_authenticated:
            data['author'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Posted!'})
        return Response({'error': serializer.errors})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['POST'])
@permission_classes([AllowAny])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        data = request.data.copy()
        data['post'] = post_id
        data['anonymous'] = True
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Commented!'})
        return Response({'error': serializer.errors})
    except:
        return Response({'error': 'Post not found'})
