from django.urls import path
from room.views import StatisticsViewSet, StatisticsMiniBarViewSet

urlpatterns = [
    path('statistics/', StatisticsViewSet.as_view(), name='statistics'),
    path('statistics-minibar/', StatisticsMiniBarViewSet.as_view(), name='statistics'),
]