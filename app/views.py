from functools import cache
import os
import uuid
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.urls import reverse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from operator import itemgetter
from .utils import get_top_tracks, session_cache_path

MESSAGE_TAGS = {
    constants.ERROR: '',
    40: 'danger'
}

os.environ["SPOTIPY_CLIENT_ID"] = "72de6f3abdc24383a58e4b56cfb14e14"
os.environ["SPOTIPY_CLIENT_SECRET"] = "f5f9fbe5d9a64d11896e7dc42bd901ed"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8000/"



SCOPE = "user-library-read user-read-recently-played user-top-read playlist-modify-public"

def index(request):
    if not request.session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        request.session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path= session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=SCOPE,
        cache_handler=cache_handler, 
        show_dialog=True
    )
    
    # 3 then 2, the order is necessary
    if request.GET.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render(request, "app/landing_page.html", {
            "auth_url": auth_url
        })

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Played but neither were saved or added to a playlist
    recently_played = spotify.current_user_recently_played(limit=5)["items"]
    liked_tracks = spotify.current_user_saved_tracks(limit=5)["items"]
            
    return render(request, "app/index.html", {
        "info": spotify.me(),
        "recently_played": recently_played,
        "liked_tracks": liked_tracks
    })

def add(request, **kwargs):
    # Check if logged in
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    user_id = spotify.me()["id"]

    if request.method == "POST":
        # Server-side validation if no songs were chosen
        if not request.POST.getlist("track_id"):
            message = "You have to choose atleast one song, c'mon!"
            print(messages.ERROR)
            messages.add_message(request, messages.ERROR, message)
            return redirect(reverse("add", kwargs={"type": kwargs.get("type")}))

        # Create the playlist or retrive it if name given
        if request.POST["playlist-type"] == "create":
            # For creating new playlist
            playlist = spotify.user_playlist_create(user_id, request.POST["new-playlist-name"], public=True)
            message = "New playlist made, enjoy!"
        else:
            # For adding in existing playlist
            playlist = spotify.user_playlist(user_id, request.POST["playlist-type"])
            message = "Recents were added to the playlist, enjoy!"

        spotify.user_playlist_add_tracks(user_id, playlist["id"], request.POST.getlist("track_id"))

        # Success
        messages.success(request, message)
        return redirect(reverse("add", kwargs={"type": kwargs.get("type")}))

    # Set limit of songs to be fetched from api according to user input
    limit = 5
    if kwargs.get("limit"):
        limit = kwargs.get("limit") + 5
        # Don't let user ask for more than 50 songs
        if limit > 50:
            messages.error(request, "You can't see more than 50 songs, sorry :-(")
            return redirect(reverse("show_more", kwargs={"type": kwargs.get("type"), "limit": 45}))
    
    # Get songs according to the kwargs given
    if kwargs.get("type") == "liked":
        tracks = spotify.current_user_saved_tracks(limit=limit)["items"]
    elif kwargs.get("type") == "recent":
        tracks = spotify.current_user_recently_played(limit=limit)["items"]
    playlists = spotify.user_playlists(user_id)
    return render(request, "app/add.html", {
        "tracks": tracks,
        "type": kwargs.get("type"),
        "playlists": playlists,
    })

def taste(request):
    # Check if logged in 
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    data = get_top_tracks(spotify)
    return render(request, "app/your_taste.html", {
        "best_of_all": data["best_of_all"],
        "top5s": data["top5s"],
        "top_artists": data["top_artists"]
    })

def sign_out(request):
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path(request))
        request.session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


    
