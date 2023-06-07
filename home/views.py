from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import HouseTable
from .models import FilteringHousetTable
from django.db.models import Q
from django.http import JsonResponse
import json
from . import preprocessing

# Create your views here.

def index(request):
    house_list = FilteringHousetTable.objects.order_by()
    house_list_before = HouseTable.objects.order_by()

    context = {
                'house_list': house_list,
                'house_list_before': house_list_before
              }
    
    # Page from the theme 
    return render(request, 'pages/dashboard.html', context)

def accessDB(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if data[2] == "전세":
            if data[1] == None:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(houseType = data[2]) & Q(housePrice = data[3]) & Q(agentName = data[6]))
            else:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(jibun = data[1]) & Q(houseType = data[2]) & Q(housePrice = data[3]) & Q(agentName = data[6]))

            estimateprice = preprocessing.calculate_weighted_average([float(result[0].latitude), float(result[0].longtitude)], "전세")

            context = {
                "latitude" : result[0].latitude,
                "longtitude": result[0].longtitude,
                "예상 전세 보증금 가격": estimateprice,
                "house_type": "전세"
            }

            print(estimateprice)
        elif data[2] == "월세":
            if data[1] == None:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(houseType = data[2]) & Q(housePrice = data[3]) & Q(monthlyPrice = data[4]) & Q(agentName = data[6]))
            else:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(jibun = data[1]) & Q(houseType = data[2]) & Q(housePrice = data[3]) & Q(monthlyPrice = data[4]) & Q(agentName = data[6]))

            estimateprice, estimateprice2 = preprocessing.calculate_weighted_average([float(result[0].latitude), float(result[0].longtitude)], '월세')

            context = {
                "latitude" : result[0].latitude,
                "longtitude": result[0].longtitude,
                "예상 월세 보증금 가격": estimateprice,
                "예상 월세 가격": estimateprice2,
                "house_type": "월세"
            }

            print(estimateprice, " ", estimateprice2)
        elif data[2] == "매매":
            if data[1] == None:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(houseType = data[2]) & Q(memePrice = data[5]) & Q(agentName = data[6]))
            else:
                result = HouseTable.objects.filter(Q(address = data[0]) & Q(jibun = data[1]) & Q(houseType = data[2]) & Q(memePrice = data[5]) & Q(agentName = data[6]))

            estimateprice = preprocessing.calculate_weighted_average([float(result[0].latitude), float(result[0].longtitude)], '매매')

            context = {
                "latitude" : result[0].latitude,
                "longtitude": result[0].longtitude,
                "예상 매매 가격": estimateprice,
                "house_type": "매매"
            }

            print(estimateprice)

        print(result[0].latitude, " ", result[0].longtitude)

    return JsonResponse(context)


def houseListTable(request):
    
    selected_address = request.GET.get('selected_address', None)

    houses = FilteringHousetTable.objects.filter(address=selected_address)
    house_list = list(houses.values('address', 'jibun', 'houseType', 'housePrice', 'monthlyPrice', 'memePrice', 'agentName'))

    return JsonResponse({'house_list': house_list})