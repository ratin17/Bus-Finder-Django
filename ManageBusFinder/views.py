from django.shortcuts import render,redirect
from django.contrib import messages

from Buses.models import OrderingModel,Bus
from Stands.models import Stand,Area
from FindBus.models import Suggestion
from .models import Log,LogCount

from BusData.areas import AreaData
from BusData.stands import StandData
from BusData.buses import BusData



from django.contrib.auth.decorators import login_required


from datetime import datetime
from datetime import timedelta


# Create your views here.



@login_required
def suggestions(request):
    return render(request,'suggestions.html')
    


@login_required
def allSuggestions(request):
    suggestions=Suggestion.objects.all()
    print(suggestions)
    context = {'suggestions': suggestions}
    return render(request, 'show-suggestions.html', context)


@login_required
def readSuggestions(request):
    suggestions=Suggestion.objects.filter(isRead=True)
    context = {'suggestions': suggestions}
    return render(request, 'show-suggestions.html', context)




@login_required
def unreadSuggestions(request):
    suggestions=Suggestion.objects.filter(isRead=False)
    context = {'suggestions': suggestions}
    return render(request, 'show-suggestions.html', context)


@login_required
def readSuggestion(request,id):
    suggestion=Suggestion.objects.get(id=id)
    if suggestion:
        suggestion.isRead=True
        suggestion.save()
    return redirect('manage:all-suggestions')


@login_required
def deleteSuggestion(request,id):
    suggestion=Suggestion.objects.get(id=id)
    if suggestion:
        suggestion.delete()
    return redirect('manage:all-suggestions')





@login_required
def logs(request):
    logCount=LogCount.objects.get(id=1).count
    context = {'logCount': logCount}
    return render(request,'logs.html',context)
    


@login_required
def allLogs(request):
    logs=Log.objects.all()
    # print(logs)
    logCount=LogCount.objects.get(id=1).count
    context = {'logs': logs,'logCount': logCount}
    return render(request, 'show-logs.html', context)



@login_required
def typeLogs(request,type,):
    
    logs=Log.objects.filter(type=type)
    # print(type,logs)
    logCount=LogCount.objects.get(id=1).count
    context = {'logs': logs,'type':type,'logCount': logCount}
    return render(request, 'show-logs.html', context)


@login_required
def keepLogsOfLast_X_DaysOrHoursOrMinutes(request,n,choice):
    
    now=datetime.now()
    
    if choice=='days':
        deleteBefore=now-timedelta(days=n)
    elif choice=='hours':
        deleteBefore=now-timedelta(hours=n)
    elif choice=='minutes':
        deleteBefore=now-timedelta(minutes=n)
        
    logs=Log.objects.filter(time__lte=deleteBefore)
    if logs:
        logs.delete()
    
    return redirect('manage:all-logs')


@login_required
def deleteLogsOfLast_X_DaysOrHoursOrMinutes(request,n,choice):
    now=datetime.now()
    
    if choice=='days':
        deleteBefore=now-timedelta(days=n)
    elif choice=='hours':
        deleteBefore=now-timedelta(hours=n)
    elif choice=='minutes':
        deleteBefore=now-timedelta(minutes=n)
        
    logs=Log.objects.filter(time__gte=deleteBefore)
    if logs:
        logs.delete()
    
    return redirect('manage:all-logs')


@login_required
def keepLatest_X_Logs(request,n):
    
    logs=Log.objects.all()
    
    if len(logs)>n:
        logs=logs[n:]
        
        for log in logs:
            log.delete()
        
    return redirect('manage:all-logs')


@login_required
def deleteLogsOfType_X(request,type):
    
    logs=Log.objects.filter(type=type)
    # print(type,logs)
    if logs:
        logs.delete()
    
    return redirect('manage:all-logs')



@login_required
def deleteAll(request):
    logs=Log.objects.all()
    if logs:
        logs.delete()
    
    return redirect('manage:all-logs')









# ------------ Danger Zone Starts -----------------



@login_required
def manage(request):
    return render(request,'manage.html')




@login_required
def removeData(request):
    
    OrderingModel.objects.all().delete()
    messages.success(request,"All Ordering-Model Data deleted")
    
    Bus.objects.all().delete()
    messages.success(request,"All Bus Data deleted")
    
    Stand.objects.all().delete()
    messages.success(request,"All Stand Data deleted")
    
    Area.objects.all().delete()
    messages.success(request,"All Area Data deleted")
    
    
    
    headerMsg="Remove Data"
    processMsg="Deleting all Data from All Models ... ... ... ..."
    successMsg="All Models are CLEAN now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)


@login_required
def addAreas(request):
    
    incoming=len(AreaData)
    count=0
    
    for key,area in AreaData.items():
        a=Area.objects.create(a_no=int(key),a_name=area["name"])
        if(a):count=count+1
        messages.success(request,f"{a.a_name} Created Succesfully !")
        
        # messages.success(request,f"{area["name"]} {type(area["name"])} Created Succesfully !")
    messages.success(request,f"{count} of {incoming} Area objects Created Succesfully !")
    
    headerMsg="Add Areas"
    processMsg="Adding All Areas ... ... ... ..."
    successMsg="All Areas are ADDED now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)



@login_required
def addStands(request):
    
    incoming=len(StandData)
    count=0
    
    areas=Area.objects.all()
    for key,stand in StandData.items():
        s=Stand.objects.create(s_no=int(key),s_name=stand["standName"],lati=stand["lati"],longi=stand["longi"],trafficCof=stand["traffic"])
        
        if(s):
            count=count+1
            messages.success(request,f"{s.s_name} Created Succesfully !")
        
        else:
            messages.warning(request,f'---- ---- >>> {stand["standName"]} Was NOT CREATED !!!!')
        
        standAreas=stand["areas"]
            
        for a in areas:
            if a.a_no in standAreas:
                s.area.add(a)
                messages.success(request,f"{a.a_name} added Succesfully to {s.s_name} !")
            
    messages.success(request,f"{count} of {incoming} Stand objects Created Succesfully !")
    
    headerMsg="Add Stands"
    processMsg="Adding All Stands ... ... ... ..."
    successMsg="All Stands are ADDED now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)



@login_required
def addBuses(request):
    
    incoming=len(BusData)
    count=0
    
    for key,bus in BusData.items():
        b=Bus.objects.create(b_no=int(key),b_name=bus["name"],rating=bus["Rating"],isActive=bus["isActive"],service=bus["service"])
        
        if(b):
            count=count+1
            messages.success(request,f"{b.b_name} Created Succesfully !")
            
        else:
            messages.warning(request,f'---- ---- >>> {bus["name"]} Was NOT CREATED !!!!')
        
        # messages.success(request,f"{bus["name"]} {type(bus["name"])} Created Succesfully !")
    
    messages.success(request,f"{count} of {incoming} Bus objects Created Succesfully !")
    
    headerMsg="Add Buses"
    processMsg="Adding All Buses ... ... ... ..."
    successMsg="All Buses are ADDED now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)




@login_required
def addBusStands(request):
    
    buses=Bus.objects.all()
    
    incomingBus=len(BusData)
    busCount=0
    totalBusStandCount=0
    
    for bus in buses:
        
        standList=BusData[str(bus.b_no)]["stands"]
        
        incomingStand=len(standList)
        standCount=0
        
        order=1
        
        for stand in standList:
            stand=Stand.objects.filter(s_no=stand).first()
            if(stand):
                bs=OrderingModel.objects.create(bus=bus,stand=stand,order=order)
                if(bs):
                    messages.success(request,f"{bs.stand.s_name} added to {bs.bus.b_name} !")
                    order=order+1
                    standCount+=1
                    totalBusStandCount+=1
                else:
                    messages.warning(request,f'---- ---- >>> {stand.s_name} Was NOT ADDED to {bus.b_name} !!!!')
                    print(f'---- ---- >>> {stand.s_name} Was NOT ADDED to {bus.b_name} !!!!')
            else:
                messages.warning(request,f"---- ---- >>> Couldn't Found any stand with Stand No {stand} !!!!")
                print(f"---- ---- >>> Couldn't Found any stand with Stand No {stand} !!!!")
        
        messages.success(request,f"*** *** {standCount} of {incomingStand} Bus-Stands added to {bus.b_name}!")
        print(f"*** *** {standCount} of {incomingStand} Bus-Stands added to {bus.b_name}!")
        
        busCount+=1
    
    messages.success(request,f"### ### {totalBusStandCount} Bus-Stands added to {busCount} of {incomingBus} Bus objects Created Succesfully !")
        
    
    
    headerMsg="Add Bus-Stands"
    processMsg="Adding All Bus-Stands ... ... ... ..."
    successMsg="All Bus-Stands are ADDED now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)



@login_required
def configure(request):
    
    OrderingModel.objects.all().delete()
    messages.success(request,"All Ordering-Model Data deleted")
    
    Bus.objects.all().delete()
    messages.success(request,"All Bus Data deleted")
    
    Stand.objects.all().delete()
    messages.success(request,"All Stand Data deleted")
    
    Area.objects.all().delete()
    messages.success(request,"All Area Data deleted")
    
    for area in AreaData.values():
        a=Area.objects.create(a_name=area["name"])
        messages.success(request,f"{a.a_name} Created Succesfully !")
        
        # messages.success(request,f"{area["name"]} {type(area["name"])} Created Succesfully !")
        
    areas=Area.objects.all()
    for stand in StandData.values():
        s=Stand.objects.create(s_name=stand["standName"],lati=stand["lati"],longi=stand["longi"])
        
        standAreas=stand["areas"]
        stringAreas=[]
        for standArea in standAreas:
            stringAreas.append(AreaData[str(standArea)]["name"])
            
        for a in areas:
            if a.a_name in stringAreas:
                s.area.add()
            
        messages.success(request,f"{s.s_name} Created Succesfully !")
        
        # messages.success(request,f"{stand[0]} {type(stand[0])} Created Succesfully !")
        
        
    for bus in BusData.values():
        b=Bus.objects.create(b_name=bus["name"])
        messages.success(request,f"{b.b_name} Created Succesfully !")
        
        # messages.success(request,f"{bus["name"]} {type(bus["name"])} Created Succesfully !")
        
        
    
    headerMsg="Configure Database"
    processMsg="Configuring All Models ... ... ... ..."
    successMsg="All Models are Re-Configured now !"
    
    context={'headerMsg':headerMsg,'processMsg':processMsg,'successMsg':successMsg}
    return render(request,'configure.html',context)