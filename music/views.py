from django.views import generic
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import operator
from functools import reduce

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('music:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'album_list'
    paginate_by = 9
    def get_queryset(self):
        return Album.objects.all()

class AlbumSearch(IndexView, LoginRequiredMixin):
    paginate_by = 9
    def get_queryset(self):
        result = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(album_title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(artist__icontains=q) for q in query_list))
            )

        return result

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
   

class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = [ 'album_title', 'artist','genre','album_logo' ]

class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = [ 'album_title', 'artist','genre','album_logo' ]

class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongList(LoginRequiredMixin, generic.ListView):
    model = Song
    context_object_name = 'song_list'
    template_name = 'music/songlist.html'
    paginate_by = 10

class SongSearch(SongList, LoginRequiredMixin):
    paginate_by = 10
    def get_queryset(self):
        result = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(album__album_title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(song_title__icontains=q) for q in query_list))
            )

        return result



class SongDetail(LoginRequiredMixin, generic.DetailView):
    model = Song
    context_object_name = 'song_detail'
    template_name = 'music/songdetail.html'       

    
