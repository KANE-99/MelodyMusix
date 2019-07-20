from django.db import models
from django.urls import reverse


# Create your models here.
class Album(models.Model):
    album_title = models.CharField(max_length = 250)
    artist = models.CharField(max_length = 250)
    genre = models.CharField(max_length = 250)
    album_logo = models.FileField()
    

    def get_absolute_url(self):
        return reverse('music:detail' , kwargs={ 'pk': self.pk})
    def __str__(self):
        return self.album_title +" By "+self.artist


def user_directory_path(instance, filename):
    return f"{str(instance.album).replace(' ','-') }/{filename}"

class Song(models.Model):
    album = models.ForeignKey(Album,on_delete = models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    upload = models.FileField(upload_to=user_directory_path)
    duration = models.CharField(max_length=10, default="00:00")
    
    def __str__(self):
        return self.song_title