from django.urls import path
from .views import VideoList, GetVideoChunk

urlpatterns = [
    path('video/', VideoList.as_view()),
    path('video/<str:pk>', GetVideoChunk.as_view()),
    # path('hello/', GetVideoChunk.as_view()),

]
