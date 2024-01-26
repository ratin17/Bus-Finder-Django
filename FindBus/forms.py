from django import forms
from Buses.models import Bus
from Stands.models import Stand

class BusFinderForm(forms.Form):
    dept = forms.ModelChoiceField(queryset=Stand.objects.all(), empty_label=None)
    dest = forms.ModelChoiceField(queryset=Stand.objects.all(), empty_label=None)