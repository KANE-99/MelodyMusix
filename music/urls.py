from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'music'

urlpatterns = [
    path('', IndexView.as_view(), name = "index" ),
    path('<int:pk>', DetailView.as_view() , name = "detail"),
    path('album/add',AlbumCreate.as_view(),name = "album-add"),
    path('album/<int:pk>',AlbumUpdate.as_view(),name = "album-update"),
    path('album/<int:pk>/delete',AlbumDelete.as_view(),name = "album-delete"),
    path('song/add',SongCreate.as_view(),name = "song-add"),
    path('song/<int:pk>',SongUpdate.as_view(),name = "song-update"),
    path('song/<int:pk>/delete',SongDelete.as_view(),name = "song-delete"),
    path('songs', SongList.as_view(), name= "song-list"),
    path('song/<int:pk>', SongDetail.as_view(), name= "song-detail"),
    path('search/album',AlbumSearch.as_view(),name="album-list-view"),
    path('search/song',SongSearch.as_view(),name="song-list-view"),
] 
