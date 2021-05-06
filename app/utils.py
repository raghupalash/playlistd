import os
import pprint

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path(request):
    return caches_folder + request.session.get('uuid')

def get_top_tracks_and_artists(spotify):
    data = {} # Data to be sent
    top_long_term = spotify.current_user_top_tracks(limit=5, time_range="long_term")["items"]
    top_medium_term = spotify.current_user_top_tracks(limit=1, time_range="medium_term")["items"]
    top_short_term = spotify.current_user_top_tracks(limit=5, time_range="short_term")["items"]
    top_artists = spotify.current_user_top_artists(limit=10, time_range="medium_term")["items"]

    # Group data together the way it will be displayed
    data["top_artists"] = top_artists
    # List of best song from each category
    best_of_all = [top_long_term[0], top_medium_term[0], top_short_term[0]]
    # Headings for the sections
    best_song_headers = [
        "Song that got you through all ups and downs",
        "Your unofficial favourite?",
        "Your new found Love"
    ]
    data["best_of_all"] = zip(best_of_all, best_song_headers)
    top5s_headers = [
        "Tracks you don't seem to get enough of these days",
        "Your All Time Favourites!"
    ]
    top5s = [top_short_term, top_long_term]
    data["top5s"] = zip(top5s, top5s_headers)

    return data
    
def add_to_playlist(**kwargs):
    """ Add tracks to a playlist(new or existing) and returns a message given spotify, tracks, 
        playlist_id(can also have a value of 'create'), user_id"""

    spotify = kwargs.get("spotify")
    # Create the playlist or retrive it if name given
    if kwargs.get("playlist_id") == "create":
        # Create a new playlist
        try:
            playlist = spotify.user_playlist_create(kwargs.get("user_id"), kwargs.get("new_playlist"), public=True)
            playlist_id = playlist["id"]
            message = "New playlist made, enjoy!"
            status = "success"
        except:
            message = "Couldn't make new playlist, sorry :-("
            status = "error"
            return message, status
    else:
        # For adding in existing playlist
        playlist_id = kwargs.get("playlist_id")
        message = "Recents were added to the playlist, enjoy!"
        status = "success"

    try:
        spotify.user_playlist_add_tracks(kwargs.get("user_id"), playlist_id, kwargs.get("tracks"))
    except:
        message = "Couldn't add tracks to the playlist, sorry :-("
        status = "error"
        

    return message, status
