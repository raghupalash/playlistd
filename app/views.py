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
from .utils import get_top_tracks, get_top_artists_and_genres, session_cache_path, add_to_playlist

MESSAGE_TAGS = {
    constants.ERROR: '',
    40: 'danger'
}

os.environ["SPOTIPY_CLIENT_ID"] = "72de6f3abdc24383a58e4b56cfb14e14"
os.environ["SPOTIPY_CLIENT_SECRET"] = "f5f9fbe5d9a64d11896e7dc42bd901ed"
os.environ["SPOTIPY_REDIRECT_URI"] = "https://playlistd.herokuapp.com/"



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
            messages.add_message(request, messages.ERROR, message)
            return redirect(reverse("add", kwargs={"type": kwargs.get("type")}))

        message, status = add_to_playlist(
            spotify=spotify,
            user_id=user_id,
            tracks=request.POST.getlist("track_id"),
            playlist_id=request.POST["playlist-type"],
            new_playlist=request.POST["new-playlist-name"]
        )

        # Success
        if status == "success":
            messages.success(request, message)
        else:
            messages.add_message(request, messages.ERROR, message)
            
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
        results = spotify.current_user_saved_tracks(limit=limit)["items"]
        tracks = [result["track"] for result in results]
    elif kwargs.get("type") == "recent":
        results = spotify.current_user_recently_played(limit=limit)["items"]
        tracks = [result["track"] for result in results]
    elif kwargs.get("type") == "top_tracks_long":
        tracks = spotify.current_user_top_tracks(limit=limit, time_range="long_term")["items"]
        pprint.pprint(tracks)
    elif kwargs.get("type") == "top_tracks_short":
        tracks = spotify.current_user_top_tracks(limit=limit, time_range="short_term")["items"]

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
    tracks = get_top_tracks(spotify)
    artists = get_top_artists_and_genres(
        spotify, 
        time_range="medium_term",
        artist_limit=10,
        genre_limit=5,
    )
    return render(request, "app/your_taste.html", {
        "best_of_all": tracks["best_of_all"],
        "top5s": tracks["top5s"],
        "top_artists": artists["top_artists"],
        "genres": artists["top_genres"]
    })

def edit(request, **kwargs):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
        
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    user_id = spotify.me()["id"]

    if request.method == "POST":
        # Remove the tracks
        try:
            spotify.playlist_remove_all_occurrences_of_items(
                request.POST["playlist_id"], 
                request.POST.getlist("track_id")
            )
        except:
            messages.error(request, "Unable to remove the tracks :-(")
            return redirect(reverse("edit", kwargs={"id":request.POST["playlist_id"]}))

    if kwargs.get("id"):
        try:
            results = spotify.playlist_items(kwargs.get("id"), limit=100, offset=0)
            tracks = results["items"]
            while results["next"]:
                results = spotify.next(results)
                tracks.extend(results["items"])
            return render(request, "app/edit_tracks.html", {
                "playlist_id": kwargs.get("id"),
                "tracks": tracks
            })
        except:
            messages.error(request, "Unable to retrieve tracks :-(")
            return redirect(reverse("edit"))

    playlists = spotify.user_playlists(user_id)
    return render(request, "app/edit.html", {
        "playlists": playlists["items"],
    })

def magic(request):
    """ Currently not in function """
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Recommendations on the basis of top artists
    top_artists_genres = []
    time_ranges = ["long_term", "medium_term", "short_term"]
    for time_range in time_ranges:
        top_artists_genres.append(get_top_artists_and_genres(
            spotify, 
            time_range=time_ranges,
            artist_limit=10,
            genre_limit=5,
        ))
    top_artists = []
    top_genres = []
    for item in top_artists_genres:
        top_artists.extend(item["top_artists"])

    top_artists_id = [artists["id"] for artists in top_artists][:5]
    recommendation = [] # 6 element on list (3 for artists, 3 for genres)
    recommendation.extend(spotify.recommendations(seed_artists=top_artists_id, limit=5))
    print(recommendation[0])
    return redirect("/")    

    
def sign_out(request):
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path(request))
        request.session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


    
