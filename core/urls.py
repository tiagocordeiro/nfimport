from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/avatar/', views.avatar_update, name='avatar_update'),
    path('signup/', views.signup, name='signup'),
]
