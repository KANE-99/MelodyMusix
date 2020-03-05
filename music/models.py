from django.db import models
from django.urls import reverse
from django.conf import settings
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import math

# Create your models here.
def album_logo_path(instance, filename):
    return f"{str(instance.owned_by).replace(' ','-')}/albums/image/{filename}"

class Album(models.Model):
    album_title = models.CharField(max_length = 250)
    artist = models.CharField(max_length = 250)
    genre = models.CharField(max_length = 250)
    album_logo = models.FileField(upload_to = album_logo_path)
    owned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length = 150, default="")
    
    def get_absolute_url(self):
        return reverse('music:detail' , kwargs={ 'pk': self.pk})
    def __str__(self):
        return self.album_title +" By "+self.artist

def user_directory_path(instance, filename):
    return f"{str(instance.owned_by).replace(' ','-') }/albums/{str(instance.album).replace(' ','-') }/{filename}"

class Song(models.Model):
    album = models.ForeignKey(Album,on_delete = models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    upload = models.FileField(upload_to=user_directory_path)
    # duration = models.CharField(max_length=10, default="00:00")
    owned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    @property
    def duration(self):
        if(self.file_type=="mp3"):
            length = MP3(self.upload.path).info.length
        else:
            length = MP4(self.upload.path).info.length
        minutes = math.floor(length/60)
        seconds_int = length - minutes*60
        if(seconds_int >= 10):
            seconds_str = str(seconds_int)
        else:
            seconds_str = '0'+str(seconds_int)
        seconds = seconds_str[0:2]
        time = str(minutes) + ':' + seconds
        
        return time
    def get_absolute_url(self):
        return reverse('music:detail' , kwargs={ 'pk': self.album.pk})
    def __str__(self):
        return self.song_title