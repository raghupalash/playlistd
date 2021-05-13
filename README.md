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
* This project is sufficiently distinct from the other projects in this course, it uses spotify API at it's core
..* Most of the functionality is based on interaction with spotify, nothing of this sort was in any other project
of the course.
* This project utilises Django with 2 models on the backend (for making api requests and other logic)
* JavaScript is used in like functionality and also used in some buttons to hide and display certian sections.
* This web app is completely mobile responsive(infact the design looks much better on mobile)




