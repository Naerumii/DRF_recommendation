import csv
import requests
import pandas as pd
import random
from datetime import datetime

now = datetime.now()

filename = 'ratings.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)

titles = ['userId', 'storeId', 'rating', 'timestamp']
writer.writerow(titles)

for i in range(100):
    storeid_set = random.sample(range(200), 150)
    storeid_set.sort()

    userid = i
    for j in range(150):
        storeid = storeid_set[j]
        rating = random.randrange(1, 6)
        nowtime = now.timestamp()
        rating_data = [userid, storeid, rating, nowtime]
        writer.writerow(rating_data)