from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_events),
    path('add/', views.add_event),
]