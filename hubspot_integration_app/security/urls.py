from django.urls import path, include
from security import views


urlpatterns = [
    path('oauth_callback', views.oauth_callback),
]
