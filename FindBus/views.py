from django.shortcuts import render,redirect
from .models import Suggestion
from .forms import BusFinderForm
from Buses.models import Bus,OrderingModel
from Stands.models import Stand
from django.contrib import messages
from Stands.views import haversine

import math
from django.utils import timezone

MPK=5 # should not change
BRC=5 # Can be changed if want to change bus rating priority

Holiday=[
    #Index Escaper
    [],
    
    
    #january
    [],
    
    #february
    [21],
    
    
    #march
    [17,26],
    
    #april
    [7,10,11,12,13,14],
    
    #may
    [1,23],
    
    #june
    [17,18,19,20],
    
    #july
    [],
    
    #august
    [15],
    
    #september
    [16],
    
    #october
    [12,16],
    
    #november
    [],
    
    #december
    [16,25]
    
]

timeMap=[
    
    # 0 Monday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':1.3,'9':1.3,'10':1.2,'11':1.2,'12':1.2,'13':1.1,'14':1.2,'15':1.3,'16':1.4,'17':1.4,'18':1.5,'19':1.6,'20':1.6,'21':1.4,'22':1.2,'23':0.7},
    
    # 1 Tuesday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':1.3,'9':1.3,'10':1.2,'11':1.2,'12':1.2,'13':1.1,'14':1.2,'15':1.3,'16':1.4,'17':1.4,'18':1.5,'19':1.6,'20':1.6,'21':1.4,'22':1.2,'23':0.7},
    
    # 2 Wednesday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':1.3,'9':1.3,'10':1.2,'11':1.2,'12':1.2,'13':1.1,'14':1.2,'15':1.3,'16':1.4,'17':1.4,'18':1.5,'19':1.6,'20':1.6,'21':1.4,'22':1.2,'23':0.7},
    
    # 3 Thursday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':1.3,'9':1.3,'10':1.2,'11':1.2,'12':1.2,'13':1.1,'14':1.2,'15':1.3,'16':1.4,'17':1.4,'18':1.5,'19':1.6,'20':1.6,'21':1.4,'22':1.2,'23':0.7},
    
    # 4 Friday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':0.8,'9':0.8,'10':0.8,'11':0.7,'12':0.7,'13':0.8,'14':0.8,'15':0.9,'16':1.0,'17':1.0,'18':1.1,'19':1.2,'20':1.2,'21':1.2,'22':1.1,'23':0.7},
    
    # 5 Saturday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':0.9,'9':1.0,'10':0.9,'11':0.7,'12':0.7,'13':0.8,'14':0.8,'15':0.9,'16':1.0,'17':1.0,'18':1.1,'19':1.2,'20':1.2,'21':1.2,'22':1.1,'23':0.7},
    
    # 6 Sunday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':1.3,'9':1.3,'10':1.2,'11':1.2,'12':1.2,'13':1.1,'14':1.2,'15':1.3,'16':1.4,'17':1.4,'18':1.5,'19':1.6,'20':1.6,'21':1.4,'22':1.2,'23':0.7},
    
    # 7 Holiday
    {'0':0.6,'1':0.5,'2':0.5,'3':0.5,'4':0.5,'5':0.5,'6':0.6,'7':0.8,'8':0.8,'9':0.8,'10':0.8,'11':0.7,'12':0.7,'13':0.8,'14':0.8,'15':0.9,'16':1.0,'17':1.0,'18':1.1,'19':1.2,'20':1.2,'21':1.2,'22':1.1,'23':0.7},
]

def distCalculator(route):
    count=0.0
    for i in range(1,len(route)):
        # stand1_lati=route[i-1].
        if route[i-1].lati and route[i-1].longi and route[i].lati and route[i].longi:
            count+=haversine(route[i-1].lati,route[i-1].longi,route[i].lati,route[i].longi)
    count=count/1000
    count=round(count,2)
    return count


def getTimeCo():
    
    UtcTime = timezone.now()
    currentTime = UtcTime.astimezone(timezone.get_current_timezone())
    
    day=currentTime.weekday()
    date=currentTime.now().date().day
    month=currentTime.now().date().month
    
    if date in Holiday[month]:
        day=7
    hour=currentTime.hour
    
    # print(hour)
    
    timeCof=timeMap[day][str(hour)]
    
    # print("Time Co-efficient: ",timeCof)
    return timeCof

def busFinder(request):
    if request.method == 'POST':
        form = BusFinderForm(request.POST)
        if form.is_valid():
            dept=form.cleaned_data['dept']
            dest=form.cleaned_data['dest']
            # print("!!!!!!!!!! Form is valid !!!!!!!!!!!!")
            if dept == dest:
                messages.success(request,"Departure and Destination Can't be Same !")
                return render(request,'result.html')
            
            # print(dept)
            # print(dest)
            
            return redirect('result', dept.id, dest.id)
            
    
    else:
        form = BusFinderForm()
        

    return render(request, 'bus_finder.html', {'form': form})


def result(request,id1,id2):
    
    dept=Stand.objects.filter(id=id1).first()
    dest=Stand.objects.filter(id=id2).first()
    # print(dept)
    timeCof=getTimeCo()
            
    resBuses=[]
    buses=Bus.objects.all()
    for bus in buses:
        
        bus_ordering=bus.orderingmodel_set.order_by('order')
        # print('-- --- -- ',bus.b_name)
        stands=[]

        for b in bus_ordering:
            
            stands.append(b.stand)
        
                
        # print(stands)
        if (dept in stands) and (dest in stands):
            # print('// // // // ',bus.b_name)
            d={}
            d['bus']=bus
            
            
            dept_index=stands.index(dept)
            dest_index=stands.index(dest)
            
            if dept_index<dest_index:
                d['route']=stands[dept_index:dest_index+1]
            elif dest_index==0:
                d['route']=stands[dept_index::-1]
            else:
                d['route']=stands[dept_index:dest_index-1:-1]
            
            d['dist']=distCalculator(d['route'])
            
            revRat=100-bus.rating
            busMpk=MPK+((revRat/100)*BRC)
            busTime=busMpk*d['dist']*timeCof
            
            if busTime>=60:   
                busHour=int(busTime//60)
            else:
                busHour=0
                
            busMinute=math.ceil(busTime%60)
            
            if busHour>0 and busHour<2:
                d['busTime']=f'{busHour} Hour, {busMinute} Minutes'
            elif busHour and busHour>0:
                d['busTime']=f'{busHour} Hours, {busMinute} Minutes'
            else:
                d['busTime']=f'{busMinute} Minutes'
                
            resBuses.append(d)
            
    # print(resBuses)            
    context = {'buses': resBuses, 'dept':dept, 'dest':dest}
    
    return render(request,'result.html',context)



def suggest_bus_stand(request,bus_id,stand_id):
    
    bus=Bus.objects.filter(id=bus_id).first()
    stand=Stand.objects.filter(id=stand_id).first()
    
    if bus and stand:
        order=OrderingModel.objects.filter(bus=bus,stand=stand).first().order
        if order:
            context={'bus':bus,'stand':stand,'order':order}
            return render(request, 'suggest_bus_stand.html', context)
        else:
            context={'error':f"Order is not Found !"}
    else:
        context={'error':f"Bus or Stand is not Found !"}
       
    return render(request, 'error.html', context)

def suggest_bus(request,bus_id):
    
    bus = Bus.objects.get(id=bus_id)
    
    if bus:
    
        bus_ordering=bus.orderingmodel_set.order_by('order')
        
        stands=[]

        for b in bus_ordering:
            stands.append(b.stand)
        

        context = {'bus': bus, 'stands': stands}
        return render(request, 'suggest_bus.html', context)
        
    else:
        context={'error':f"Bus is not Found !"}
       
    return render(request, 'error.html', context)


def create_suggestion(request,switch,p1,p2,p3,p4):
    
    if switch==1:
        bus=Bus.objects.filter(id=p1).first()
        stand=Stand.objects.filter(id=p2).first()
        
        if bus and stand:
            title=f"{bus.b_name} Doesn't Go through {stand.s_name} !"
            Suggestion.objects.create(title=title,s_type='predefinned')
            return redirect('success_suggestion','success')
        else:
            return redirect('success_suggestion','error')
        
    elif switch==2:
        bus=Bus.objects.filter(id=p1).first()
        stand=Stand.objects.filter(id=p2).first()
        
        if bus and stand:
            title=f"{bus.b_name} Goes through {stand.s_name} but Order Should not be {p3} !"
            Suggestion.objects.create(title=title,s_type='predefinned')
            return redirect('success_suggestion','success')
        else:
            return redirect('success_suggestion','error')
        
    elif switch==3:
        bus=Bus.objects.filter(id=p1).first()
        
        if bus:
            title=f"Bus Name ( {bus.b_name} ) is Incorrect ! "
            headline=f"Suggestion for {{ bus.b_name }} Submitted Successfully !"
            Suggestion.objects.create(title=title,s_type='predefinned')
            return redirect('feedback',headline,title,'success')
        else:
            return redirect('success_suggestion','error')
    
    return redirect('buses')


def feedback(request,msg,suggest):
    
    if suggest=='success':
        context={'suggestion':msg,'headline':"headline"}
        return render(request,'suggestion_success.html',context)