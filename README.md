# Playlistd

[Playlistd](https://playlistd.herokuapp.com/) is a 3rd party web app built on top of spotify api to help you with making playlists.
* On the _Index Page_ you can see your music taste summerised (a mini Spotify Wrapped!).
* On _Make Playlist_ section you are given your Recently Played songs and Liked songs, you can add them to your
playlists(existing or new).
* When you click on _Add to playlist_ button anywhere on the website, you are taken to a page where you can see
a list of 5 songs with a checkbox to unselect them (they are all selected by default), you can click on _show more_ link to get 5 more songs(upto 50)
* When desired songs selected click on _Add to Playlist_ then select your playlist or make a new one and voila songs are added to your playlist.
* If you want to remove songs from a playlist, head over to _edit playlist_ section.
* _explore_ section shows you public playlists of all people that have used this app, you can listen to them
and like them (this section is not available in the online version)

This project was made as a Final Project for CS50 Web Development with Python and Javascript

## How is it helpful?
The problem that I faced while using spotify was that it makes making playlist a shit tone of work, first you make a playlist, then add songs one by one, aghhhh, I hate it.
So I made this, here you can add songs that are your favourites or the songs that you recently played or liked (upto last 50 songs). But the main thing is, here you can select multiple songs to be added in your playlist(existing or a new one)!

Also Removing songs from a playlist is a shit tone of work too on spotify, here you can delete multiple songs, awesome right?

## How to Run
Install the required packages
```bash
pip install -r requirements.txt
```
Initailize Database
```bash
python manage.py makemigrations app
python manage.py migrate
```
In the project root directory run the application
```bash
python manage.py runserver
```

## How this projects satisfies the requirements set by the staff?
* This project is sufficiently distinct from the other projects in this course, it uses spotify API at it's core.
* Most of the functionality is based on interaction with spotify, nothing of this sort was in any other project
of the course.
* This project utilises Django with 2 models on the backend (for making api requests and other logic)
* JavaScript is used in like functionality and also used in some buttons to hide and display certian sections.
* This web app is completely mobile responsive(infact the design looks much better on mobile)

## Project File Structure
* __app__ is the main app that handels all the functionality of the website. It contains - 
  * static/app that contains all the static files -
    * styles.css that contains all our css styles.
    * add.js that contains javascript that will be used when we click on Add to Playlist button in 'add/', it will display all our playlist and a form to create a new playlist (which were hidden previously).
    * like.js which implements like action on explore page(Changes frontend and sends fetch request to view to change the data).
  * templates - 
    * add.html - Page that let's us select the songs to be added in playlist and select the playlist we want to add them.
    * edit_tracks.html - Page that let's us remove songs from a playlist.
    * explore.html - Page were all playlists of all users(who have used this app) with link to the playlist and option to like them.
    * index.html - Page after login is complete, gives you a list of your favourites(mini 'Spotify Wrapped').
    * landing_page.html - Sign in page.
    * layout.html - Has code that is shared by all other templates.
    * playlists.html - Renders when you click on _Make Playlists_, gives you a list of recently playes songs and liked songs.
  * templatetags - 
    * custom_tags.py - Creates a custom tag to go on _Make Playlist_ section with an id of a particular section (recently played or liked).
  * Procfile and runtime.txt are used for hosting on Heroku.
  

