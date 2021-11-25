from django.db.models.aggregates import Avg
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.core import serializers as django_serializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

from .models import Country, Genre, Movie, Actor, Vote
from .serializers import CountrySerializer, MovieListSerializer, MovieSerializer, VoteSerializer

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_countries(request):
    country_objs = Country.objects.all()
    serializer = CountrySerializer(country_objs, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country(request, country_pk):
    country_obj = get_object_or_404(Country, pk=country_pk)
    serializer = CountrySerializer(country_obj)
    
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_movies(request, country_pk):
    movie_objs = get_list_or_404(Movie, country=country_pk)
    serializer = MovieListSerializer(movie_objs, many=True)

    for i, data in enumerate(serializer.data):
        vote_obj = Movie.objects.get(pk=data['id']).vote.filter(user=request.user)
        if vote_obj.exists():
            serializer.data[i]['is_voted'] = vote_obj[0].vote_score
        else:
            serializer.data[i]['is_voted'] = 0

    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vote_movie(request):
    movie = get_object_or_404(Movie, pk=request.data.get('movie'))

    vote_obj = request.user.vote.filter(movie=movie)
    request.data['user'] = request.user.pk
    
    if vote_obj.exists():
        vote_obj = vote_obj[0]
        serializer = VoteSerializer(data=request.data, instance=vote_obj)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            diff = vote_obj.vote_score - int(request.data.get('vote_score'))
            total_score = movie.vote_average * movie.vote_count - diff
            movie.vote_average = total_score/movie.vote_count
            movie.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            total_score = movie.vote_average * movie.vote_count
            movie.vote_count+=1
            movie.vote_average = total_score/movie.vote_count
            movie.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_recommends(request):
    page_num = request.GET.get('page')
    # 없을 때 기본 값
    vote_average = 4 if not request.user.vote.all() \
                    else request.user.vote.aggregate(vote_average=Avg('vote_score'))['vote_average']

    min_vote_average = vote_average-1
    max_vote_average = vote_average+1
    
    movie_objs = Movie.objects.filter(Q(vote_average__gte=min_vote_average)&Q(vote_average__lt=max_vote_average))
    
    paginator = Paginator(movie_objs, per_page=8, )
    if int(page_num) > paginator.num_pages:
        return HttpResponse(django_serializer.serialize('json', []), content_type='application/json')
    page_obj = paginator.get_page(page_num)

    data = django_serializer.serialize('json', page_obj)

    return HttpResponse(data, content_type='application/json')


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    
    return Response(serializer.data)

from ast import literal_eval
import itertools
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny])
def add_data(request):
    with open('country_list.csv', 'r') as f:
        country_objs = []
        for data in f.readlines()[1:]:
            data = data.rstrip().split('\t')
            country_objs.append(
                Country(kr_name=data[1], en_name=data[2], flag=data[-3], 
                            thumbnail=data[3], thumbnail_title=data[4], thumbnail_content=data[5], 
                            capital=data[6], lat=data[7], lng=data[8], capital_kr=data[-2], utc=data[-1],)
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
    
    return JsonResponse({'state':True})
