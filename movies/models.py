from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    kr_name = models.CharField(max_length=32)
    en_name = models.CharField(max_length=32)
    flag = models.URLField(max_length=256)
    thumbnail = models.URLField(max_length=300)
    thumbnail_title = models.CharField(max_length=128)
    thumbnail_content = models.TextField()
    capital = models.CharField(max_length=32)
    capital_kr = models.CharField(max_length=16)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    utc = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return self.en_name


class Movie(models.Model):
    title = models.CharField(max_length=128)
    released_date = models.DateField()
    poster_path = models.CharField(max_length=128)
    vote_average = models.FloatField()
    vote_count = models.PositiveIntegerField()
    director = models.CharField(max_length=64)
    overview = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='movies', null=True)

    def __str__(self) -> str:
        return self.title
    

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vote')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='vote')
    vote_score = models.SmallIntegerField()

    def __str__(self) -> str:
        return f'{self.user.nickname} {self.movie.title} {self.vote_score}'