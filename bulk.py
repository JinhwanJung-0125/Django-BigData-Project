import os
import django
import csv
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import HouseTable

f = open('total 3.csv', 'r', encoding = 'cp949')
info = []

rdr = csv.reader(f)
next(rdr)

for row in rdr:
    idx,address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude = row

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

    if housePrice == 'None':
        housePrice = None
    else:
        housePrice = int(housePrice)

    if monthlyPrice == 'None':
        monthlyPrice = None
    else:
        monthlyPrice = int(monthlyPrice)

    if memePrice == 'None':
        memePrice = None
    else:
        memePrice = int(memePrice)

    if recommend == '[]':
        recommend = False
    elif recommend == "['추천']":
        recommend = True

    tuple = (address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude)
    info.append(tuple)

f.close()

instances = []

for (address, jibun, jungong, houseType, floors, housePrice, monthlyPrice, memePrice, currentlyUpdate, firstUpdate, recommend, agentName, agentAddress, agentNumber, latitude, longtitude) in info:
    instances.append(HouseTable(address = address, jibun = jibun, jungong = jungong, houseType = houseType, floors = floors, housePrice = housePrice, monthlyPrice = monthlyPrice, memePrice = memePrice, currentlyUpdate = currentlyUpdate, firstUpdate = firstUpdate, recommend = recommend, agentName = agentName, agentAddress = agentAddress, agentNumber = agentNumber, latitude = latitude, longtitude = longtitude))

print(instances)

HouseTable.objects.bulk_create(instances)