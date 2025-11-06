from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Item, Chat
from .serializers import ItemSerializer

def bot_reply(msg):
    msg = msg.lower()
    if 'lost' in msg:
        return "Describe item: color, place?"
    elif 'found' in msg:
        return "Upload photo! Where found?"
    return "Say 'lost phone' or 'found keys'"

@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    try:
        msg = request.data.get('message', '')
        session, _ = Chat.objects.get_or_create(id=1)
        session.messages.append({'user': msg})
        reply = bot_reply(msg)
        session.messages.append({'bot': reply})
        session.save()
        return Response({'reply': reply, 'chat': session.messages[-5:]})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def items(request):
    if request.method == 'GET':
        return Response(ItemSerializer(Item.objects.filter(claimed=False), many=True).data)
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response({'msg': 'Posted!'})
    return Response({'error': serializer.errors})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim(request, id):
    try:
        item = Item.objects.get(id=id)
        item.claimed = True
        item.save()
        return Response({'msg': 'Claimed!'})
    except:
        return Response({'error': 'Not found'})