from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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