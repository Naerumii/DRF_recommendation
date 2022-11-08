from django.urls import path
from recommend import views

urlpatterns = [
    path('', views.RecommendView.as_view(), name='recommend_view'),
]