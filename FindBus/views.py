from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Suggestion
from .forms import BusFinderForm,SuggestionForm
from Buses.models import Bus,OrderingModel
from Stands.models import Stand
from django.contrib import messages
from Stands.views import haversine

import math
from django.utils import timezone

MPK=5 # should not be changed
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
    
    dept=get_object_or_404(Stand,id=id1)
    dest=get_object_or_404(Stand,id=id2)
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
            d['obj']=bus
            
            
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


def suggestResult(request,dept_id,dest_id,bus_id,dist,busTime):
    
    dept = Stand.objects.get(id=dept_id)
    dest = Stand.objects.get(id=dest_id)
    bus = Bus.objects.get(id=bus_id)
    
    if bus and dept and dest:
    
        bus_ordering=bus.orderingmodel_set.order_by('order')
        
        stands=[]

        for b in bus_ordering:
            stands.append(b.stand)
        

        dept_index=stands.index(dept)
        dest_index=stands.index(dest)
        
        if dept_index<dest_index:
            stands=stands[dept_index:dest_index+1]
        elif dest_index==0:
            stands=stands[dept_index::-1]
        else:
            stands=stands[dept_index:dest_index-1:-1]
        
        context = {'bus': bus, 'stands': stands,'dept':dept,'dest':dest,'dist':dist,'busTime':busTime}
        print(context)
        return render(request, 'suggest_result.html', context)
        
    else:
        context={'error':f"Bus or Stands are not Found !"}
       
    return render(request, 'error.html', context)



def suggestCustom(request):
    
    if request.method=="POST":
        form=SuggestionForm(data=request.POST)
        if form.is_valid():
            new_suggestion=form.save(commit=False)
            new_suggestion.s_type='custom'
            new_suggestion.save()
            msg=new_suggestion.title
            # print(msg)
            return redirect('feedback_custom',msg)
        else:
            msg="Error during the submission of Custom-suggestion !"
            return redirect('feedback_error',msg)
    else:
        form=SuggestionForm()
        context={'form':form}
    return render(request,'suggestion_custom.html',context)



def suggestBusStand(request,bus_id,stand_id):
    
    bus=get_object_or_404(Bus,id=bus_id)
    stand=get_object_or_404(Stand,id=stand_id)
    
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



def suggestBus(request,bus_id):
    
    bus=get_object_or_404(Bus,id=bus_id)
    
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



def suggestStand(request,stand_id):
    
    stand = Stand.objects.get(id=stand_id)
    
    
    if stand:
        context = {'stand': stand}
        return render(request, 'suggest_stand.html', context)
        
    else:
        context={'error':f"Stand is not Found with id = {stand_id} !"}
       
    return render(request, 'error.html', context)



def feedbackCustom(request,msg):
    
    context={'suggestion':msg,'headline':"Custom Suggestion Submitted !"}
    return render(request,'feedback_custom.html',context)



def feedbackSuccess(request,msg,headline):

    Suggestion.objects.create(title=msg,s_type='predefinned')
    
    context={'suggestion':msg,'headline':f"Suggestion Submitted for {headline} !"}
    return render(request,'feedback_success.html',context)



def feedbackError(request,msg):
    
    context={'suggestion':msg,'headline':"Error !"}
    return render(request,'feedback_error.html',context)