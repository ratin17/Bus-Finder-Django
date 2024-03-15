from django import forms

from .models import Area,Stand

class StandForm(forms.ModelForm):

    class Meta:
        model = Stand
        fields = ['s_no','s_name','lati','longi','area']
        labels = {'s_name': 'Stand Name:','lati':'Latitude:','longi':'Longitude:','area':'Select Area:'}



class AreaForm(forms.ModelForm):
    
    class Meta:
        model = Area
        fields = ['a_name']
        labels = {'a_name': 'Area Name:'}
        
