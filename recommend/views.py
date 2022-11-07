from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from recommend.serializers import RecommendSerializer
from users.models import User
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from recommend.models import Restaurant
from rest_framework.generics import get_object_or_404

# Create your views here.
class RecommendView(APIView):
    def get(self, request):
        userid = request.user.id  # 현재 사용자 pk(지금은 5번)
        print(userid)
        # csv 파일읽기
        restaurants = pd.read_csv('jeju_restaurants.csv')
        ratings = pd.read_csv('ratings.csv')

        # 상점번호(storeId)를 기준으로 ratings와 restaurants를 결합
        restaurant_ratings = pd.merge(ratings, restaurants, on='storeId')

        # user별로 식당에 부여한 rating 값을 볼 수 있도록 pivot table 사용
        title_user = restaurant_ratings.pivot_table('rating', index='userId', columns='storeId')
        # 평점을 부여안한 식당 그냥 0이라고 부여
        title_user = title_user.fillna(0)

        # 유저 0~99 번과 유저 0~99 번 간의 코사인 유사도를 구함
        user_based_collab = cosine_similarity(title_user, title_user)
        # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
        user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)

        # 현재 유저와 가장 비슷한 유저를 뽑고,
        sim_user = user_based_collab[userid].sort_values(ascending=False).loc[:10].index[1]
        # 유사한 유저가 좋아했던 식당 평점 내림차순으로 출력
        result = title_user.query(f"userId == {sim_user}").sort_values(ascending=False, by=sim_user, axis=1)
        result_me = title_user.query(f"userId == {userid}").sort_values(ascending=True, by=userid, axis=1)
        # 현재 유저(접속자)와 가장 유사한 유저의 좋은 평점 중 1번 사용자가 가지 않은 식당 고르기(5개?)
        # recommend_list에 추천할 식당번호가 저장
        count = 0
        recommend_list = []
        for i in range(200):
            if count < 5:
                if result_me[result.columns[i]].values[0] == 0.0:
                    recommend_list.append(result.columns[i])
                    count += 1
            else:
                break

        print(recommend_list)

        # 해당 id값의 식당 db 정보 가져오기
        store_result=[]    
        for i in recommend_list:
            try:
                store = Restaurant.objects.get(id=i+1)
                store_result.append(store)
            except:
                pass
        
        print(store_result)
        serializer = RecommendSerializer(store_result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # recommends = Article.objects.filler(id=duskkkhsf)
        # serializer = ArticleSerializer(articles, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)