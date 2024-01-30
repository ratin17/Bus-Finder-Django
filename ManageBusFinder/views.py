from django.shortcuts import render
from django.contrib import messages

from Buses.models import OrderingModel,Bus
from Stands.models import Stand,Area

from BusData.source import AreaData

# Create your views here.

def manage(request):
    return render(request,'manage.html')


def configure(request):
    
    OrderingModel.objects.all().delete()
    messages.success(request,"All Ordering-Model Data deleted")
    
    Bus.objects.all().delete()
    messages.success(request,"All Bus Data deleted")
    
    Stand.objects.all().delete()
    messages.success(request,"All Stand Data deleted")
    
    Area.objects.all().delete()
    messages.success(request,"All Area Data deleted")
    
    for areas in AreaData.values():
        for area in areas:
            a=Area.objects.create(a_name=area)
            messages.success(request,f"{a.a_name} Created Succesfully !")
            
    
    return render(request,'configure.html')