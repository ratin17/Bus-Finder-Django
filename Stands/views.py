from django.shortcuts import render,redirect
from .models import Stand,Area
from .forms import StandForm,AreaForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required




from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def stands(request):
    
    stands = Stand.objects.all()
    print('##### ### ',stands)
    
    context = {'stands': stands}
    return render(request, 'stands.html', context)


def stand(request,stand_id):
    stand= Stand.objects.get(id=stand_id)
    buses=stand.bus_set.all()
    
    context = {'stand': stand, 'buses': buses}
    
    return render(request, 'stand.html', context)


@login_required
def new_stand(request):
    if request.method == 'POST':
    
        form = StandForm(data=request.POST)
        
        if form.is_valid():
            
            stands = Stand.objects.all()
            
            name=form.cleaned_data['s_name']
            lat=form.cleaned_data['lati']
            lon=form.cleaned_data['longi']
            
            for stand in stands:
                if stand.s_name==name:
                    print("Already Added with this name")
                    form = StandForm()
                    context = {'form': form}
                    messages.error(request, f'Already Added {stand.id}.{stand.s_name} !!')
                    return render(request, 'new_stand.html', context)
                elif lat and lon and stand.lati and stand.longi:
                    dis=haversine(stand.lati,stand.longi,lat,lon)
                    if(dis<50):
                        print(f"Very Much Nearby with {stand.s_name} ! ")
                        form = StandForm()
                        context = {'form': form}
                        messages.error(request, f'Very Much Nearby with {stand.s_name} !! ')
                        return render(request, 'new_stand.html', context)
                    
            form.save()
            return redirect('stands:stands')
    else:
        form = StandForm()
        context = {'form': form}
    return render(request, 'new_stand.html', context)



@login_required
def new_area(request):
    if request.method == 'POST':
    
        form = AreaForm(data=request.POST)
        
        if form.is_valid():
            
            areas = Area.objects.all()
            
            name=form.cleaned_data['a_name']
            
            for area in areas:
                if area.a_name==name:
                    print("Already Added with this name")
                    form = AreaForm()
                    context = {'form': form}
                    messages.error(request, 'Already Added f"{area.id}.{area.a_name} "!!')
                    return render(request, 'new_area.html', context)
                    
            form.save()
            return redirect('stands:stands')
    else:
        form = AreaForm()
        context = {'form': form}
    return render(request, 'new_area.html', context)

@login_required
def edit_stand(request,stand_id):
    stand=Stand.objects.get(id=stand_id)
    
    if request.method != 'POST':
        form = StandForm(instance=stand)
    
    else:
        
        # orderingIns=get_object_or_404(OrderingModel,id=orderingmodel_id)
        
        form = StandForm(instance=stand,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('stands:stands')
    
    context = {'form': form,'stand':stand}
    return render(request, 'edit_stand.html', context)



    