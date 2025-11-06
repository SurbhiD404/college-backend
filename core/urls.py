from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', views.profile),
    path('logout/', views.logout_view),
    path('update/', views.update_user_view),
    path('create-admin/', views.create_admin, name='create_admin'),
]