from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils import timezone
from taggit.managers import TaggableManager


class Group(models.Model):
    name = models.CharField(max_length=128)
    member1 = models.CharField(max_length=128, null=True, blank=True)
    member2 = models.CharField(max_length=128, null=True, blank=True)
    member3 = models.CharField(max_length=128, null=True, blank=True)
    member4 = models.CharField(max_length=128, null=True, blank=True)
    member5 = models.CharField(max_length=128, null=True, blank=True)
    member6 = models.CharField(max_length=128, null=True, blank=True)
    member7 = models.CharField(max_length=128, null=True, blank=True)
    portrait = models.ImageField(upload_to='groups/', null=True, blank=True)
    formed = models.IntegerField()
    history = models.FileField(upload_to='histories/', blank=True, null=True)
    # songs

    def __str__(self):
        return self.name

    def url_detail(self):
        return reverse('rock:group-detail', kwargs={
            'pk': self.id,
        })

    class Meta:
        ordering = ['name']

class Song(models.Model):
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    rating = models.FloatField(default=5.0)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    group = models.ForeignKey(Group, related_name='songs', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    trailer = models.CharField(max_length=11, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    tags = TaggableManager()
    wishing_to_listen = models.ManyToManyField(User, blank=True, related_name='playlist')
    # user_ratings

    def __str__(self):
        return self.title

    def url_detail(self):
        return reverse('rock:song-detail', kwargs={
            'slug': self.slug,
        })

    def genres_str(self):
        return ' '.join(t.name for t in self.tags.all())

    def number_of_other_wishing_to_listen(self):
        return self.wishing_to_listen.count() - 1

    def users_made_rating(self):
        return User.objects.filter(ratings__song=self).all()

    class Meta:
        ordering = ['title']


class Addon(models.Model):
    user = models.OneToOneField(User, related_name='addon', on_delete=models.CASCADE)
    userpic = models.ImageField(upload_to='userpics/', blank=True, null=True)


class Comment(models.Model):
    text = models.CharField(max_length=512)
    song = models.ForeignKey(Song, related_name='comments', on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published']

