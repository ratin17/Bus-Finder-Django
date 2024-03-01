from django import forms
from Buses.models import Bus
from Stands.models import Stand

class BusFinderForm(forms.Form):
    dept = forms.ModelChoiceField(queryset=Stand.objects.all(), label="From :",empty_label=None)
    dest = forms.ModelChoiceField(queryset=Stand.objects.all(),label="To :", empty_label=None)