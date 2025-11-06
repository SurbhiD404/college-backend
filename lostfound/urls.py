from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat),
    path('items/', views.items),
    path('claim/<int:id>/', views.claim),
]