from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles import serializers
from articles.models import Article, Comment
from django.db.models.query_utils import Q
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, ArticleUpdateSerializer, CommentSerializer, CommentCreateSerializer


#유준 댓글
#댓글 불러오기, 댓글 달기
class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#댓글수정, 댓글 삭제
class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        #본인인지 확인
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)  

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

#게시글 전부 보기 demo
class ArticleView(APIView):
    #게시글 전부 가져오기
    def get(self, request):
        #article 전부 가져오고
        articles = Article.objects.all()
        #시리얼라이즈해주기, 전부다 가져와서 ,many = True
        serializer = ArticleListSerializer(articles, many = True)
        #시리얼라이즈 된 데이터 넣기
        return Response(serializer.data, status = status.HTTP_200_OK)

    #게시글 새로 쓰기

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#팔로우 목록 보기 demo
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = Q()
        #지금 접속한 사람이 팔로우한 모든 사람 조건문으로 갖고옴
        for user in request.user.followings.all():
            q.add(Q(user=user), q.OR)
        feeds = Article.objects.filter(q)
        serializer = ArticleListSerializer(feeds, many=True)
        return Response(serializer.data)

#게시글 상세보기 demo
class ArticleDetailView(APIView):
    #특정 게시글 불러오기(그냥보기)
    def get(self, request, article_id):
        #특정 아이디 값만 가져오기

        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, article_id):
        print(request.user)
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user: #접속자와 작성자가 다르면 수정못하게 에러코드 
            serializer = ArticleUpdateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("삭제완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

#팔로우 기능 demo
class LikeView(APIView):
    #한번 팔로우 두번 언팔로우
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요취소 했습니다.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요했습니다.", status=status.HTTP_200_OK)