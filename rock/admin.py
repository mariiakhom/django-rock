from django.contrib import admin

from .models import *

class SongInLine(admin.TabularInline):
    model = Song
    prepopulated_fields = {"slug": ["title", "group"]}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [SongInLine]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'year', 'rating', 'genres_str']
    prepopulated_fields = {"slug": ["title", "group"]}


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'text', 'published']

