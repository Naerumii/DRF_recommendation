from rest_framework import serializers
from recommend.models import Restaurant

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("store_name", "store_image", "store_rating", "store_address")