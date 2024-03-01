from django.shortcuts import render
from .forms import BusFinderForm
from Buses.models import Bus
from django.contrib import messages
from Stands.views import haversine

def distCalculator(route):
    count=0.0
    for i in range(1,len(route)):
        # stand1_lati=route[i-1].
        if route[i-1].lati and route[i-1].longi and route[i].lati and route[i].longi:
            count+=haversine(route[i-1].lati,route[i-1].longi,route[i].lati,route[i].longi)
    count=count/1000
    count=round(count,2)
    return count


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
                        
                    resBuses.append(d)
                           
            context = {'buses': resBuses, 'dept':dept, 'dest':dest}
            return render(request,'result.html',context)
    
    else:
        form = BusFinderForm()

    return render(request, 'bus_finder.html', {'form': form})

def result(request):
    return render(request,'result.html',)