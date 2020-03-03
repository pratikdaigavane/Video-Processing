from django.urls import path
from .views import VideoList

urlpatterns = [
    path('video/', VideoList.as_view()),
]
