from django.urls import path, include
from deals.views import DealListAPIView, HomeView, SyncDealsData


urlpatterns = [
    path('', DealListAPIView.as_view()),
    path('home', HomeView.as_view()),
    path('sync_data', SyncDealsData.as_view())
]
