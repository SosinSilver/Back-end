from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def get_list(request):
    pass


@api_view(['POST'])
def article_create(request):
    pass


@api_view(['POST'])
def comment_create(request, article_pk):
    pass


# @api_view(['GET'])
# def get_comments(request, article_pk):
#     pass


@api_view(['POST'])
def like(request, article_pk):
    pass