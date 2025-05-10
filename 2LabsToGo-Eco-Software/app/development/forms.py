from django.forms import ModelForm
from django import forms
from .models import *


class Development_Form(forms.ModelForm):
    class Meta:
        model = Development_Db
        fields = ['filename', 'method']

class PlateProperties_Form(forms.ModelForm):

    class Meta:
        model = PlateProperties_Db
        fields = ['size_x','size_y','offset_left','offset_right','offset_bottom']

class DevelopmentBandSettings_Form(forms.ModelForm):


    class Meta:
        model = BandSettings_Dev_Db
        fields = ['volume', 'fluid', 'applications', 'printBothways','waitTime', 'density', 'viscosity', 'description']

    def clean(self):
        if self.cleaned_data.get('printBothways'):
            self.cleaned_data['printBothways']="True"
        else:
            self.cleaned_data['printBothways']="False"
        return self.cleaned_data

class PressureSettings_Form(forms.ModelForm):

       class Meta:
        model = PressureSettings_Dev_Db
        fields = ['temperature','nozzlediameter','pressure','motor_speed']


class Flowrate_Form(forms.ModelForm):
    class Meta:
        model = Flowrate_Db
        fields = ['value']


class ZeroPosition_Form(forms.ModelForm):

    class Meta:
        model = ZeroPosition_Db
        fields = ['zero_x','zero_y']


