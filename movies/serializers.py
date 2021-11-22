from django.db.models.aggregates import Count
from rest_framework import serializers
from .models import Movie, Country, Vote, Actor, Genre


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)


    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('country',)


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'movie', 'vote_score')

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path')


class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = '__all__'
