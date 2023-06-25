from django.urls import path

from . import views

app_name = 'rock'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('song/list/', views.SongListView.as_view(), name='song-list'),
    path('song/<slug:slug>/', views.SongDetailView.as_view(), name='song-detail'),
    path('group/list/', views.GroupListView.as_view(), name='group-list'),
    path('group/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),

    path('user/sign/out/', views.user_sign_out, name='user-sign-out'),
    path('login/page', views.login_page, name='login-page'),
    path('user/sign/in/', views.user_sign_in, name='user-sign-in'),

    path('search/', views.search, name='search'),
    path('song/comment/<int:pk>/', views.add_comment, name='add-comment'),
    path('song/playlist/<int:pk>/', views.change_playlist_song_status, name='playlist-change'),

    path('api/song/list/', views.SongListAPIView.as_view(), name='api-song-list'),
]