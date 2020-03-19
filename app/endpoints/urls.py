from django.urls import path

from .views import VideoList, GetVideoChunk, ChangeAudio

urlpatterns = [
    path('video/', VideoList.as_view(), name='video-list'),
    path('video/<str:pk>', GetVideoChunk.as_view(), name='chunk-list'),
    path('video/<str:pk>/<int:chunk_no>',
         ChangeAudio.as_view(),
         name='change-audio'),
]
