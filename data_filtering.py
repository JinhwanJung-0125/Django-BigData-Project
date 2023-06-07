import pandas as pd

df = pd.read_csv('total 3.csv', encoding='cp949')

start_date = '2023-01-01'
end_date = '2023-05-31'

filtered_df = df[(df['최초 계시 날짜'] >= start_date) & (df['최초 계시 날짜'] <= end_date)]

print(filtered_df)

filtered_df.to_csv('게시날짜.csv', encoding='cp949')

import os
import django
import csv
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import FilteringHousetTable

f = open('게시날짜.csv', 'r', encoding = 'cp949')
info = []

rdr = csv.reader(f)
next(rdr)

for row in rdr:
    idx, _, address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude = row

    idx = int(idx)

    jungong = jungong[: -3]

    jungong = re.sub('[.]|[/]|[-]|[,]', '', jungong)
    
    floors = floors[: -1]
    
    if floors == '반지하':
        floors = 0
    elif floors == '옥탑방':
        floors = -1
    else:
        floors = int(floors)

    if housePrice == '':
        housePrice = None
    else:
        housePrice = int(float(housePrice))

    if monthlyPrice == '':
        monthlyPrice = None
    else:
        monthlyPrice = int(float(monthlyPrice))

    if memePrice == '':
        memePrice = None
    else:
        memePrice = int(float(memePrice))

    if recommend == '[]':
        recommend = False
    elif recommend == "['추천']":
        recommend = True

    tuple = (address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude)
    info.append(tuple)

f.close()

instances = []

for (address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude) in info:
    instances.append(FilteringHousetTable(address = address, jibun = jibun, jungong = jungong, houseType = houseType, floors = floors, housePrice = housePrice, monthlyPrice = monthlyPrice, memePrice = memePrice, currentlyUpdate = currentlyUpdate, firstUpdate = firstUpdate, recommend = recommend, agentName = agentName, agentAddress = agentAddress, agentNumber = agentNumber, latitude = latitude, longtitude = longtitude))

print(instances)

FilteringHousetTable.objects.bulk_create(instances)