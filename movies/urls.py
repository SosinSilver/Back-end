from django.urls import path
from . import views

urlpatterns = [
    path('country/<int:country_pk>', views.get_country),
    path('movies/<int:country_pk>', views.get_movies),
    path('recommend/', views.get_recommends),
    path('movie/<int:movie_pk>/', views.get_movie),
]
