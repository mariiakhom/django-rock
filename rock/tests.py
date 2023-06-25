from django.test import TestCase

from .models import Group, Song

class GroupSongTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Skillet')
        for i in range(5):
            Song.objects.create(title=f'Song-{i}', group=Group.objects.get(id__exact=1))



    def test_1(self):
        number_of_groups = Group.objects.count()
        self.assertEqual(number_of_groups, 3)

    def test_2(self):
        number_of_songs = Song.objects.count()
        self.assertEqual(number_of_songs, 3)

