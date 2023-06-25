from django.contrib.auth import logout, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Avg, Count
from django.db.models import Q

from rest_framework import generics

from random import choice

from .models import *
from .serializers import *
from .forms import *


class HomeView(TemplateView):
    template_name = 'rock/index.html'
    extra_context = {
        # 'songs': Song.objects.all(),
        'songs': Song.objects.order_by('-rating')[:4],
        'groups': Group.objects.annotate(rating=Avg('songs__rating')).order_by('-rating')[:3],
    }


class SongListView(ListView):
    model = Song
    paginate_by = 3


class GroupListView(ListView):
    model = Group
    queryset = Group.objects.annotate(rating=Avg('songs__rating')).order_by('name')


class SongDetailView(DetailView):
    model = Song
    # extra_context = {
    #     'c_form': CommentForm(),
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['c_form'] = CommentForm()
        context['similar_songs'] = Song.objects.filter(tags__in=self.object.tags.all()).distinct()\
            .exclude(id=self.object.id).annotate(number_of_tags=Count('tags')).order_by('-number_of_tags')[:3]
        return context


class GroupDetailView(DetailView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['rating'] = self.object.songs.aggregate(Avg('rating')).get('rating__avg')
        songs = self.object.songs.all()
        context['songs'] = songs
        trailers = self.object.songs.values_list('trailer', flat=True)
        # print(trailers)
        if trailers:
            context['trailer'] = choice(trailers)
        print([context])
        return context

def user_sign_out(request):
    next = request.GET.get('next')
    print('next', next)
    logout(request)
    return HttpResponseRedirect(next)


def login_page(request):
    next = request.GET.get('next')
    return render(request,
                  template_name='rock/login_page.html',
                  context= {
                      'next': next,
                  })


def user_sign_in(request):
    next = request.POST.get('next')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(next)
    else:
        return render(request,
               template_name='rock/login_page.html',
               context={
                   'next': next,
                   'message': 'Incorrect username or password',
                   'last_username': username,
               })


def change_playlist_song_status(request, pk):
    song = Song.objects.get(pk=pk)
    user = request.user
    if song.wishing_to_listen.contains(user):
        song.wishing_to_listen.remove(user)
    else:
        song.wishing_to_listen.add(user)
    return HttpResponseRedirect(song.url_detail())


class SongListAPIView(generics.ListAPIView):
    serializer_class = SongSerializer1
    queryset = Song.objects.all()


def search(request):
    search_str = request.POST.get('search')
    option = request.POST.get('option')
    next = request.POST.get('next')
    if search_str:
        songs = Song.objects.filter(Q(title__icontains=search_str)) if option in '13' else None
        groups = Group.objects.filter(Q(name__icontains=search_str))\
                            .annotate(rating=Avg('songs__rating')).order_by('name') if option in '23' else None
        return render(request,
                      template_name='rock/search_page.html',
                      context={
                          'search': search_str,
                          'songs': songs,
                          'groups': groups,
                      })
    else:
        return HttpResponseRedirect(next)


def add_comment(request, pk):
    song = Song.objects.get(pk=pk)
    f = CommentForm(request.POST)
    if f.is_valid():
        new_comment: Comment = f.save(commit=False)
        print('new_comment', new_comment)
        new_comment.song = song
        new_comment.user = request.user
        new_comment.save()
    else:
        print(f.errors)
    return HttpResponseRedirect(song.url_detail())