from django.views import generic
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'album_list'
    def get_queryset(self):
        return Album.objects.all()

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

class UserFormView(LoginRequiredMixin, View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, { 'form' : form } )

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('music:index')
        return render(request, self.template_name, { 'form' : form} )

class SongList(LoginRequiredMixin, generic.ListView):
    model = Song
    context_object_name = 'song_list'
    template_name = 'music/songlist.html'


class SongDetail(LoginRequiredMixin, generic.DetailView):
    model = Song
    context_object_name = 'song_detail'
    template_name = 'music/songdetail.html'       

    
