from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import HouseTable

# Create your views here.

def index(request):
    house_list = HouseTable.objects.order_by()
    context = {'house_list': house_list}
    
    # Page from the theme 
    return render(request, 'pages/dashboard.html', context)