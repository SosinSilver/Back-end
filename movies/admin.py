from django.contrib import admin

from .models import Genre, Actor, Country, Movie, Vote

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Movie)
admin.site.register(Vote)