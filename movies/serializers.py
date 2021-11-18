from django.db.models.aggregates import Count
from rest_framework import serializers
from .models import Movie, Country


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('country',)


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'