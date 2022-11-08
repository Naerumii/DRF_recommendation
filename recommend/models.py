from django.db import models
# Create your models here.
class Restaurant(models.Model):
    class  Meta:
        db_table = "restaurant"
    store_name = models.CharField(max_length=100, default='')
    store_image = models.TextField(max_length=256, default='')
    store_rating = models.CharField(max_length=100, default='')
    store_category = models.CharField(max_length=100, default='')
    store_address = models.CharField(max_length=256, default='')
    store_view = models.CharField(max_length=100, default='')
    store_review = models.CharField(max_length=100, default='')