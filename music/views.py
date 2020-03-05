from django.http import HttpResponse
from django.views import generic
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from . import models
import operator
from functools import reduce


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('music:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'album_list'
    paginate_by = 9
    def get_queryset(self):
        return Album.objects.filter(owned_by=self.request.user.id)

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
    fields = [ 'album_title', 'artist','genre','album_logo','description' ]
    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.owned_by = self.request.user
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = [ 'album_title', 'artist','genre','album_logo','description' ]

class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')   

class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    fields = ['album','file_type','song_title','upload']
    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
            form = form_class(**self.get_form_kwargs())
            form.fields['album'].queryset = models.Album.objects.filter(owned_by=self.request.user)
        return form
    def post(self,request,*args,**kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.owned_by = self.request.user
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class SongUpdate(LoginRequiredMixin, UpdateView):
    model = Song
    fields = ['album','file_type','song_title','upload']

class SongDelete(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = reverse_lazy('music:song-list')   

class SongList(LoginRequiredMixin, generic.ListView):
    model = Song
    context_object_name = 'song_list'
    template_name = 'music/songlist.html'
    paginate_by = 10
    def get_queryset(self):
        return Song.objects.filter(owned_by=self.request.user.id)

class SongSearch(SongList, LoginRequiredMixin):
    paginate_by = 10
    def get_queryset(self):
        result = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                # reduce(operator.and_,
                #        (Q(album__album_title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(song_title__icontains=q) for q in query_list))
            )

        return result



class SongDetail(LoginRequiredMixin, generic.DetailView):
    model = Song
    context_object_name = 'song_detail'
    template_name = 'music/songdetail.html'       

    
