from django.shortcuts import render,redirect
from .models import Bus,OrderingModel
from .forms import BusForm,OrderingForm,EditBusStandForm

from django.shortcuts import get_object_or_404

# Create your views here.
def buses(request):
    
    buses = Bus.objects.all()
    
    context = {'buses': buses}
    return render(request, 'buses.html', context)


def bus(request, bus_id):
    
    bus = Bus.objects.get(id=bus_id)
    
    # stands = bus.stands.all()
    # stands_ordered=bus.orderingmodel_set.order_by('-order').values_list('stand', flat=True)
    # stands = Stand.objects.filter(pk__in=stands_ordered)
    
    bus_ordering=bus.orderingmodel_set.order_by('order')
    
    stands=[]

    for b in bus_ordering:
        info=(b.order,b.stand,b.id)
        stands.append(info)
    
    # print(bus,stands)

    context = {'bus': bus, 'stands': stands}
    
    return render(request, 'bus.html', context)


def new_bus(request):
    if request.method != 'POST':
        form = BusForm()
    else:
        form = BusForm(data=request.POST)
        if form.is_valid():
            new_bus = form.save(commit=False)
            new_bus.save()
            return redirect('buses')
    
    context = {'form': form}
    return render(request, 'new_bus.html', context)


def add_stand_for_bus(request, bus_id):
    
    bus = Bus.objects.get(id=bus_id)
    
    if request.method != 'POST':
        form = OrderingForm()
    
    else:
        
        form = OrderingForm(data=request.POST)
        if form.is_valid():
            # new_busStand = form.save(commit=False)
            order=form.cleaned_data['order']
            stand=form.cleaned_data['stand']
            
            # print('======= === = ',order)
            if order<0:
                print("Order shouldnt be Negative")
                return redirect('bus',bus_id=bus_id)
            
            orderings=bus.orderingmodel_set.order_by('order')
            qsetSize=len(orderings)
            
            for ordering in orderings:
                if ordering.stand==stand:
                    print("Already Exists")
                    return redirect('bus',bus_id=bus_id)
                
            if(order<qsetSize):
                it=order
                # print('////// //// / ',it,qsetSize)
                for i in range(qsetSize-1,it-1,-1):
                    # print('@@@@@ @@@  ',qsetSize,it)
                    orderingIns=get_object_or_404(OrderingModel,bus=bus,order=i)
                    # print('#### ###### ## ',orderingIns.order, orderingIns.stand)
                    orderingIns.order=i+1
                    orderingIns.save()
                    # print('++++++++ +++++ ++ ',orderingIns.order, orderingIns.stand)
            else:
                order=qsetSize
                
            OrderingModel.objects.create(bus=bus,stand=stand,order=order)
            # orderingIns=get_object_or_404(OrderingModel,bus=bus,stand=stand,order=order)
            # print('$$$$$$$$$$$$$ $$$ ',orderingIns.order, orderingIns.stand)
            return redirect('bus',bus_id=bus_id)
    
    context = {'form': form,'bus':bus}
    return render(request, 'add_stand.html', context)



def delete_bus_stand(request,bus_id,order):
    
    bus=Bus.objects.get(id=bus_id)
    orderingDelIns=get_object_or_404(OrderingModel,bus=bus,order=order)
    orderingDelIns.delete()
    
    orderings=bus.orderingmodel_set.order_by('order')
    
    for i in range(order+1,len(orderings)+1):
        orderingIns=get_object_or_404(OrderingModel,bus=bus,order=i)
        orderingIns.order=i-1
        orderingIns.save()
        
    return redirect('bus',bus_id=bus_id)


def edit_bus_stand(request,bus_id,order):
    orderingIns=OrderingModel.objects.get(id=order)
    
    if request.method != 'POST':
        form = EditBusStandForm(instance=orderingIns)
    
    else:
        
        # orderingIns=get_object_or_404(OrderingModel,id=orderingmodel_id)
        
        form = EditBusStandForm(instance=orderingIns,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bus',bus_id=bus_id)
    
    context = {'form': form,'bus_id':bus_id,'order_id':order}
    return render(request, 'edit_bus_stand.html', context)