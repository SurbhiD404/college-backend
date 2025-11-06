from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from rest_framework import status
@api_view(['GET'])
@permission_classes([AllowAny])
def list_events(request):
    try:
        events = Event.objects.all()
        return Response(EventSerializer(events, many=True).data)
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_event(request):
    try:
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Event added!'})
        return Response({'error': serializer.errors})
    except Exception as e:
        return Response({'error': str(e)})
