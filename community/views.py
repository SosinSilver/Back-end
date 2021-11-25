from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from django.core import serializers as django_serializer
from .serializers import ArticleSerializer, CommentSerializer
from django.core.paginator import Paginator
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_list(request):
    page_num = request.GET.get('page')
    article_objs = Article.objects.order_by('-pk')
    # print(article_objs)
    paginator = Paginator(article_objs, per_page=10)
    if int(page_num) > paginator.num_pages:
        return HttpResponse(django_serializer.serialize('json', []), content_type='application/json')
    page_obj = paginator.get_page(page_num)

    data = django_serializer.serialize('json', page_obj)
    tmp = json.loads(data)
    for d in tmp:
        # print(d)
        article = Article.objects.get(pk=int(d['pk']))
        d['fields']['nickname'] = article.user.nickname
        d['fields']['comments'] = [c.get_data() for c in article.comments.order_by('-pk')]
        d['fields']['like_count'] = article.like_users.count()
        d['fields']['is_liked'] = request.user in list(article.like_users.all())
    
    data = json.dumps(tmp)

    return HttpResponse(data, content_type='application/json')

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_update(request, article_pk):
    print(Article.objects.get(pk=article_pk))
    article = get_object_or_404(Article, pk=article_pk)
    serializer = ArticleSerializer(instance=article, data=request.data)
    if request.user == article.user:
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        Response(status=status.HTTP_401_UNAUTHORIZED)
     

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        comment = serializer.save(article=article, user=request.user)
        data = json.dumps(comment.get_data())

        return HttpResponse(data, content_type='application/json')


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        article.delete()
        return Response({ 'id': article_pk })
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return Response({ 'id': comment_pk })
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
