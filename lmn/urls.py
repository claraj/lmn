from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import views_main, views_artists, views_venues, views_notes, views_users, views_shows

# app_name = 'lmn'

urlpatterns = [

    path('', views_main.homepage, name='homepage'),

    # Venue-related
    path('venues/list/', views_venues.venue_list, name='venue_list'),
    path('venues/detail/<int:venue_pk>/', views_venues.venue_detail, name='venue_detail'),
    path('venues/artists_at/<int:venue_pk>/', views_venues.artists_at_venue, name='artists_at_venue'),
    path('venues/list/add_venue', views_venues.add_venue, name='add_venue'),
    path('artists/list/save_venue', views_venues.save_venue, name='save_venue'),
    path('artists/list/create_venue', views_venues.create_venue, name='create_venue'),

    # Note related
    path('notes/latest/', views_notes.latest_notes, name='latest_notes'), 
    path('notes/detail/<int:note_pk>/', views_notes.note_detail, name='note_detail'),
    path('notes/for_show/<int:show_pk>/', views_notes.notes_for_show, name='notes_for_show'),
    path('notes/add/<int:show_pk>/', views_notes.new_note, name='new_note'),
    path('notes/<int:note_pk>/delete', views_notes.delete_note, name='delete_note'), # delete note

    # Artist related
    path('artists/list/', views_artists.artist_list, name='artist_list'),
    path('artists/detail/<int:artist_pk>/', views_artists.artist_detail, name='artist_detail'),
    path('artists/venues_played/<int:artist_pk>/', views_artists.venues_for_artist, name='venues_for_artist'),
    path('artists/list/add_artist', views_artists.add_artist, name='add_artist'),
    path('artists/list/save_artist', views_artists.save_artist, name='save_artist'),
    path('artists/list/create_artist', views_artists.create_artist, name='create_artist'),

    # User related
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),

    # Account related
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('goodbye/', views_users.goodbye, name='goodbye'),
    path('register/', views_users.register, name='register'),

    # Show related
    path('shows/list/', views_shows.show_list, name='show_list'),
    path('shows/detail/<int:show_pk>/', views_shows.show_detail, name='show_detail'),
    path('shows/list/add_show_to_venue/<int:venue_pk>', views_shows.add_show_to_venue, name='add_show_to_venue'),
    path('shows/add_show_to_artist/<int:artist_pk>/', views_shows.add_show_to_artist, name='add_show_to_artist'),
    path('shows/create_show/', views_shows.create_show, name='create_show'),
    path('shows/save_show/', views_shows.save_show, name='save_show'),
]


