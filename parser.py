import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

filename = 'jeju_restaurants.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)

titles = ['storeId', 'store_name', 'store_image', 'store_rating', 'store_category', 'store_address', 'store_view', 'store_review']
writer.writerow(titles)

store_id = 0
for page_num in range(10):
    # range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
    keyword = "제주"
    url = f'https://www.mangoplate.com/search/{keyword}?keyword={keyword}&page={page_num+1}'
    headers = {'User-Agent': 'Chrome'}
    response = requests.get(url, headers=headers)
    print('응답 : ', response)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select("li.server_render_search_result_item > div.list-restaurant-item")
    
    for item in data:
        image= item.select_one('img').get('data-original')
        title = item.select_one('h2.title').text.replace('\n', '')
        rating =item.select_one('strong.search_point').text
        category = item.select_one('span').text
        address = item.select_one('p').text.split('-')[0]
        view = item.select_one('span.view_count').text
        review = item.select_one('span.review_count').text
        store_data = [store_id, title, image, rating, category, address, view, review]
        store_id += 1
        writer.writerow(store_data)