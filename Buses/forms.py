from django import forms

from .models import Bus,OrderingModel

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['b_name']
        labels = {'b_name': 'Bus name:'}

class OrderingForm(forms.ModelForm):
    class Meta:
        model = OrderingModel
        fields = ['stand','order']
        labels = {'stand': 'Bus Stand:', 'order':'Order:'}

class EditBusStandForm(forms.ModelForm):
    class Meta:
        model = OrderingModel
        fields = ['stand','order']
        labels = {'stand': 'Bus Stand:','order':'Order:'}