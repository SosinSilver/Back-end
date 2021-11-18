from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article',)


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True,
    )

    comment_set = CommentSerializer(
        many=True,
        read_only=True,
    )
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users')

