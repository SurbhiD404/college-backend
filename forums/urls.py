from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.list_posts),
    path('posts/create/', views.create_post),
    path('posts/<int:post_id>/comment/', views.add_comment),
]