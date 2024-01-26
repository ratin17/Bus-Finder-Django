from django.shortcuts import render
from .forms import BusFinderForm
from Buses.models import Bus

def busFinder(request):
    if request.method == 'POST':
        form = BusFinderForm(request.POST)
        if form.is_valid():
            dept=form.cleaned_data['dept']
            dest=form.cleaned_data['dest']
            # print("!!!!!!!!!! Form is valid !!!!!!!!!!!!")
            
            print(dept)
            print(dest)
            resBuses=[]
            buses=Bus.objects.all()
            for bus in buses:
                bus_ordering=bus.orderingmodel_set.order_by('order')
                # print('-- --- -- ',bus.b_name)
                stands=[]

                for b in bus_ordering:
                    stands.append(b.stand)
                print('>>>>>>>>',stands)
                if (dept in stands) and (dest in stands):
                    # print('// // // // ',bus.b_name)
                    resBuses.append(bus)
                           
            context = {'buses': resBuses, 'dept':dept, 'dest':dest}
            return render(request,'result.html',context)
    
    else:
        form = BusFinderForm()

    return render(request, 'bus_finder.html', {'form': form})

def result(request):
    return render(request,'result.html',)