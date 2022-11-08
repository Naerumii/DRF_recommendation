import os
import sys
import csv
import django

#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_tambang.settings")
django.setup()
# model import
from recommend.models import *

#읽어들일 csv 디렉토리를 각 변수에 담는다.
STORE = 'jeju_restaurants.csv'

#함수 정의하기 (row부분엔 해당 table의 row명을 적어준다.)
def store():
    with open(STORE, 'rt', encoding='UTF8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                store_name = row[1]
                store_image = row[2]
                store_rating = row[3]
                store_category = row[4]
                store_address = row[5]
                store_view = row[6]
                store_review = row[7]
                print(store_name, store_image, store_rating, store_category, store_address, store_view, store_review)
                Restaurant.objects.create(
                    store_name = store_name,
                    store_image = store_image,
                    store_rating = store_rating,
                    store_category = store_category,
                    store_address = store_address,
                    store_view = store_view,
                    store_review = store_review
                    )
    print('PRODUCT DATA UPLOADED SUCCESSFULY!')

# 함수 실행
store()