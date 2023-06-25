from rest_framework import serializers

from .models import Song, Group

class SongSerializer1(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    class Meta:
        model = Song
        fields = ['title', 'group', 'rating', 'year', 'poster']