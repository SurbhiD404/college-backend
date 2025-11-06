from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict),
    path('summarize/', views.summarize_notes),
    path('recommend/', views.recommend_events),
]