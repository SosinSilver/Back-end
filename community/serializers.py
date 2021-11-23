from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):

    # nickname = serializers.CharField(
    #     source='user.nickname',
    #     read_only=True,
    # )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article',)


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True,
    )

    comments = CommentSerializer(
        many=True,
        read_only=True,
    )

    nickname = serializers.CharField(
        source='user.nickname',
        read_only=True,
    )

    # is_liked = serializers.BooleanField(
    #     source='True',
    #     read_only=True
    # )
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users')
