from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import CustomMyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

# Create your views here.

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status = status.HTTP_201_CREATED)
        else:
            return Response({"massage":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomMyTokenObtainPairSerializer

class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated] # IsAuthenticated 로그인이 되어있는 있을때만 할수있게.
    def get(self, request):
        user = request.user
        user.is_admin = True # admin 권한을 부여하는거라 post요청에서 해줘야하는게 맞다 . 
        user.save()
        return Response("get 요청")