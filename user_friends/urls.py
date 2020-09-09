from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user_friends/', views.user_friends, name='user_friends'),
]