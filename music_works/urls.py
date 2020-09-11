from django.urls import path

from music_works.works import views

urlpatterns = [
    path("music-works", views.RetrieveMusicWork().as_view(), name="music-works"),
]
