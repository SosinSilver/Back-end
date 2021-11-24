from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.get_list),
    path('article/create/', views.article_create),
    path('article/<int:article_pk>/update/', views.article_update),
    path('article/<int:article_pk>/comment/create/', views.comment_create),
    path('article/comment/<int:comment_pk>/delete/', views.comment_delete),
    # path('article/<int:article_pk>/comments/', views.get_comments),
    path('article/<int:article_pk>/like/', views.like),
    path('article/<int:article_pk>/delete/', views.delete_article),
]
