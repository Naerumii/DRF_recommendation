from dataclasses import field
from rest_framework import serializers
from articles.models import Article, Comment
from turtle import update

#유준 댓글
#댓글 기본 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    #user를 email로 바꿔준다. user는 이제 email값이 된다.
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = Comment
        exclude = ("article", )

#댓글 만들 때 '내용'만 가져오는 시리얼라이져
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", )

#게시물 시리얼라이저 demo
class ArticleSerializer(serializers.ModelSerializer):
    #게시글 조회할 때 댓글 정보도 같이 보여주기
    user = serializers.SerializerMethodField()
    #user를 email로 바꿔준다. user는 이제 email값이 된다.
    comment_set = CommentSerializer(many=True)
    #users의 model.user의 값을 email로 해놨기 때문에 연결된 값인 email로 값을 보여준다.
    likes = serializers.StringRelatedField(many=True)

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "restaurants", "image", "content")

class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content")

#게시글 목록 시리얼라이저 demo
class ArticleListSerializer(serializers.ModelSerializer):
    #시리얼라이저 메소드 필드를 위해서 원하는 값들을 추가로 보여줄 수 있음
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Article
        fields = ("pk", "title", "image", "restaurants", "created_at", "user", "likes_count", "comments_count")
