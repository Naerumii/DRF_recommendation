from django.contrib import admin
from articles.models import Article, Comment

#admin페이지에서 2개 관리 가능
admin.site.register(Article)
admin.site.register(Comment)

