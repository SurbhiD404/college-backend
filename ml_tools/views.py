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

# import requests
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from forums.models import Post, Comment
# from django.contrib.auth.models import User


# ML_BASE_URL =  "http://10.193.42.135:8000"

# def _call_ml(endpoint: str, payload: dict):
#     try:
#         url = f"{ML_BASE_URL}{endpoint}"
#         print(f"[ML CALL] → POST {url}")
#         r = requests.post(url, json=payload, timeout=20)
#         r.raise_for_status()
#         return r.json()
#     except requests.RequestException as e:
#         return {"error": f"ML service unreachable: {str(e)}"}

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def moderate_post(request):
#     text = request.data.get("text", "").strip()
#     if not text:
#         return Response({"error": "text required"}, status=status.HTTP_400_BAD_REQUEST)
#     return Response(_call_ml("/moderate-post/", {"text": text}))

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def recommend_posts(request):
#     user = request.user
#     users = list(User.objects.values("id", "username"))
#     posts = list(Post.objects.values("id", "title", "content"))
#     interactions = list(
#         Comment.objects.filter(author=user)
#         .values("post_id")
#         .distinct()
#     )

#     payload = {
#         "user_id": user.id,
#         "users": users,
#         "posts": [{"id": p["id"], "content": p["content"] or p["title"]} for p in posts],
#         "interactions": [{"user_id": user.id, "post_id": c["post_id"]} for c in interactions],
    # }

    # return Response(_call_ml("/recommend-posts/", payload))
