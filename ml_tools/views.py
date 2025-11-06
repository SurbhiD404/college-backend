from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Profile
from events.models import Event
import numpy as np
from sklearn.linear_model import LinearRegression

# ML  Replace these with real ML models later
def predict_score(scores):
    if len(scores) < 2:
        return {'error': 'Need 2+ scores'}
    X = np.array(range(len(scores))).reshape(-1, 1)
    y = np.array(scores)
    model = LinearRegression().fit(X, y)
    pred = model.predict([[len(scores)]])[0]
    return {'predicted': round(pred, 2)}

def summarize(text):
    return text[:150] + '...'  # ML: Use real summarizer

def recommend(interests):
    events = Event.objects.all()
    recs = []
    for e in events:
        score = sum(interests.get(tag, 0) for tag in e.tags)
        if score > 1:
            recs.append({'event': e.title, 'score': score})
    return recs[:3]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    scores = request.data.get('scores', request.user.profile.previous_scores)
    result = predict_score(scores)
    request.user.profile.previous_scores = scores
    request.user.profile.save()
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def summarize_notes(request):
    text = request.data.get('notes')
    if not text:
        return Response({'error': 'Send notes!'})
    return Response({'summary': summarize(text)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_events(request):
    interests = request.data.get('interests', {})
    request.user.profile.interests = interests
    request.user.profile.save()
    return Response(recommend(interests))

