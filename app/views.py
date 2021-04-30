import os
import uuid
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from operator import itemgetter



os.environ["SPOTIPY_CLIENT_ID"] = "72de6f3abdc24383a58e4b56cfb14e14"
os.environ["SPOTIPY_CLIENT_SECRET"] = "f5f9fbe5d9a64d11896e7dc42bd901ed"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8000/"

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

SCOPE = "user-library-read user-read-recently-played user-top-read playlist-modify-public"

def index(request):
    if not request.session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        request.session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=caches_folder + request.session.get("uuid"))
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
            
    return render(request, "app/index.html", {
        "info": spotify.me(),
        "tracks": recently_played,
    })

def add(request):
    # Check if logged in
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=caches_folder + request.session.get("uuid"))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    user_id = spotify.me()["id"]


    if request.method == "POST":
        print(request.POST.getlist("track_id"))
        # Create the playlist
        playlist = spotify.user_playlist_create(user_id, "App Playlist YAY", public=True)
        tracks_id = spotify.user_playlist_add_tracks(user_id, playlist["id"], request.POST.getlist("track_id"))
        return HttpResponseRedirect("/add")

    recently_played = spotify.current_user_recently_played(limit=5)["items"]
    playlists = spotify.user_playlists(user_id)
    return render(request, "app/add.html", {
        "tracks": recently_played,
        "playlists": playlists,
    })




def sign_out(request):
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(caches_folder + request.session.get("uuid"))
        request.session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


    
