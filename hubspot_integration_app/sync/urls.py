from django.urls import path, include
from sync import views


urlpatterns = [
    path('oauth_callback', views.oauth_callback),
]
