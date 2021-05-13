from django.db import models

# Create your models here.
class User(models.Model):
    user = models.CharField(max_length=128, unique=True)


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    playlist = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_playlists")
