import json
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Country, Genre, Movie, Actor


@api_view(['GET'])
def get_country(request, country_pk):
    pass


@api_view(['GET'])
def get_movies(request, country_pk):
    pass


@api_view(['GET'])
def get_recommends(request):
    pass


@api_view(['GET'])
def get_movie(request, movie_pk):
    pass

from ast import literal_eval
import itertools
def add_data(request):
    with open('country_list.csv', 'r') as f:
        country_objs = []
        for data in f.readlines()[1:]:
            data = data.rstrip().split('\t')
            print(data)
            country_objs.append(
                Country(kr_name=data[1], en_name=data[2], flag=data[-1], 
                            thumbnail=data[3], thumbnail_title=data[4], thumbnail_content=data[5], 
                            capital=data[6], lat=data[7], lng=data[8])
            )

    Country.objects.bulk_create(country_objs)

    genre_objs = []
    with open('genres.csv', 'r') as f:
        for data in f.readlines()[1:]:
            genre_objs.append(
                Genre(name=data.rstrip())
            )
    Genre.objects.bulk_create(genre_objs)

    movie_objs = []
    genre_list = []
    actor_list = []
    with open('movie_list.csv', 'r') as f:
        for data in f.readlines()[1:]:
            data = data.rstrip().split('\t')
            country_obj = Country.objects.filter(en_name=data[-1])
            if country_obj:
                movie_objs.append(
                    Movie(title=data[1], released_date=data[6], poster_path=data[2],
                        vote_average=data[4], vote_count=data[5], director=data[9], 
                        overview=data[3], country=country_obj[0])
                )
            else:
                movie_objs.append(
                    Movie(title=data[1], released_date=data[6], poster_path=data[2],
                        vote_average=data[4], vote_count=data[5], director=data[9], 
                        overview=data[3])
                )

            genre_list.append(literal_eval(data[7]))
            actor_list.append(literal_eval(data[8]))

    Movie.objects.bulk_create(movie_objs)

    actors = list(set(list(itertools.chain(*actor_list))))
    actor_objs = []
    for actor_name in actors:
        actor_objs.append(Actor(name=actor_name))
        if len(actor_objs) > 900:
            Actor.objects.bulk_create(actor_objs)
            actor_objs = []
    
    Actor.objects.bulk_create(actor_objs)

    for i, movie in enumerate(Movie.objects.all()):
        for genre_name in genre_list[i]:
            genre_obj = Genre.objects.get(name=genre_name)
            movie.genres.add(genre_obj)
        
        for actor_name in actor_list[i]:
            actor_obj = Actor.objects.get(name=actor_name)
            movie.actors.add(actor_obj)
        movie.vote_average = round(movie.vote_average/2, 1)
        movie.save()
    
    return Response(json.dumps({'state':True}))