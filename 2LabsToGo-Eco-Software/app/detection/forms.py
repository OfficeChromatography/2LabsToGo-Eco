from django import forms
from django.forms import ModelForm
from .models import CameraControls_Db, UserControls_Db, Leds_Db, Images_Db
from django.contrib.auth.models import User

FORMATS = (('0','BMP'),    
            ('1','PNG'),
            ('2','JPEG'))

class Detection_Form(forms.ModelForm):
    class Meta:
        model = Images_Db
        fields = ['filename', 'method']

class SaveShot(forms.Form):

    name = forms.CharField(label='Name',
                    required=True,
                    max_length = 9,
                    widget=forms.TextInput(
                                        attrs={
                                                'size': '9',
                                                'placeholder':'FileName',
                                                'class':'form-control',
                                                'data-toggle':"tooltip",
                                                'data-placement':'top',
                                                'title':"Please insert a name to save your Photo",
                                                }
                                            )
                                        )

class CameraControlsForm(forms.ModelForm):
        class Meta:
            model = CameraControls_Db

            fields =[   'auto_exposure',
                        'exposure_time_absolute',
                        'white_balance_auto_preset',
                        'analogue_gain',
                        'colour_gains',
                        'imagenumber',
                        'delaytime',
                        ]
            widgets = {
                        'auto_exposure':                forms.Select(attrs={'class': 'form-control'}),
                        'white_balance_auto_preset':    forms.Select(attrs={'class': 'form-control'}),
                        }
            labels = {
                        'auto_exposure':                _('Auto Exposure:'),
                        'white_balance_auto_preset':    _('WB Preset'),
            }

        exposure_time_absolute = forms.DecimalField(label='Exposure Time (s)',
                                required=False,
                                max_digits=7,
                                decimal_places=4,
                                max_value=200,
                                min_value=0,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0.025', 'class':'form-control'}))

        analogue_gain = forms.DecimalField(label='Analogue Gain',
                                required=False,
                                max_digits=3,
                                decimal_places=1,
                                max_value=26,
                                min_value=1,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))
        
        colour_gains = forms.CharField(label='Colour Gains',
                    required=False,
                    max_length = 10,
                    widget=forms.TextInput(
                                        attrs={
                                                'size': '9',
                                                'placeholder':'1.0,1.0',
                                                'class':'form-control',
                                                'data-toggle':"tooltip",
                                                'data-placement':'top',
                                                'title':"def. 1.0,1.0",
                                                }
                                            )
                                        )

        imagenumber = forms.DecimalField(label='Number of Images',
                                required=True,
                                max_digits=3,
                                decimal_places=0,
                                max_value=200,
                                min_value=0,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1', 'class':'form-control'}))

        delaytime = forms.DecimalField(label='Delay Time between Images (s)',
                                required=True,
                                max_digits=3,
                                decimal_places=0,
                                max_value=200,
                                min_value=0,
                                widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))

        def clean_auto_exposure(self):
            auto_exposure = self.cleaned_data['auto_exposure']
            if auto_exposure:
                auto_exposure = int(auto_exposure)
            if not auto_exposure:
                auto_exposure = 0
            return auto_exposure

        def clean_exposure_time_absolute(self):
            exposure_time_absolute = self.cleaned_data['exposure_time_absolute']
            if exposure_time_absolute:
                exposure_time_absolute = exposure_time_absolute
            if not exposure_time_absolute:
                exposure_time_absolute = 0.025
            return exposure_time_absolute

        def clean_white_balance_auto_preset(self):
            white_balance_auto_preset = self.cleaned_data['white_balance_auto_preset']
            if white_balance_auto_preset:
                white_balance_auto_preset = int(white_balance_auto_preset)
            if not white_balance_auto_preset:
                white_balance_auto_preset = 0
            return white_balance_auto_preset

        def clean_analogue_gain(self):
            analogue_gain = self.cleaned_data['analogue_gain']
            if analogue_gain:
                analogue_gain = analogue_gain
            if not analogue_gain:
                analogue_gain = 1.0
            return analogue_gain

        def clean_colour_gains(self):
            colour_gains = self.cleaned_data['colour_gains']
            if colour_gains:
                colour_gains = colour_gains
            if not colour_gains:
                colour_gains = '1.0,1.0'
            return colour_gains

        def clean_imagenumber(self):
            imagenumber = self.cleaned_data['imagenumber']
            imagenumber = int(imagenumber)
            return imagenumber        

        def clean_delaytime(self):
            delaytime = self.cleaned_data['delaytime']
            delaytime = int(delaytime)
            return delaytime

class UserControlsForm(forms.ModelForm):
    class Meta:
        model = UserControls_Db
        fields = [
                     'brightness',
                       'contrast',
                     'saturation',
                      'sharpness',
        ]

    brightness = forms.DecimalField(label='Brightness (-1.0 to 1.0, where 0.0 is the default value)',
                            required=False,
                            max_digits=2,
                            decimal_places=1,
                            max_value=1,
                            min_value=-1,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'class':'form-control'}))

    contrast = forms.DecimalField(label='Contrast (0.0 to 32.0, where 1.0 is the default value)',
                            required=False,
                            max_digits=3,
                            decimal_places=1,
                            max_value=32,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1', 'class':'form-control'}))

    saturation = forms.DecimalField(label='Saturation (0.0 to 32.0, where 1.0 is the default value and 0.0 results in a greyscale image)',
                            required=False,
                            max_digits=3,
                            decimal_places=1,
                            max_value=32,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1', 'class':'form-control'}))

    sharpness = forms.DecimalField(label='Sharpness (0.0 to 16.0, where 1.0 is the default value)',
                            required=False,
                            max_digits=3,
                            decimal_places=1,
                            max_value=16,
                            min_value=0,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'1', 'class':'form-control'}))

    def clean_brightness(self):
        brightness = self.cleaned_data['brightness']
        if brightness:
            brightness = brightness
        if not brightness:
            brightness = 0
        return brightness

    def clean_contrast(self):
        contrast = self.cleaned_data['contrast']
        if contrast:
            contrast = contrast
        if not contrast:
            contrast = 1
        return contrast

    def clean_saturation(self):
        saturation = self.cleaned_data['saturation']
        if saturation:
            saturation = saturation
        if not saturation:
            saturation = 1
        return saturation

    def clean_sharpness(self):
        sharpness = self.cleaned_data['sharpness']
        if sharpness:
            sharpness = sharpness
        if not sharpness:
            sharpness = 1
        return sharpness


class ShootConfigurationForm(forms.Form):

    pixelformat = forms.ChoiceField(label='Formats', choices = FORMATS, widget=forms.Select(attrs={'class':'form-control'}))

    def clean_pixelformat(self):
        pixelformat = self.cleaned_data['pixelformat']
        pixelformat = FORMATS[int(pixelformat)][1]
        return pixelformat

MOTION_MODEL = ((0, 'Translation'),
                    (1, 'Euclidean'),
                    (2, 'Affine'),
                    (3, 'Homography'))

class AligmentConfigurationForm(forms.Form):
    warp_mode = forms.ChoiceField(label='Motion Modes', choices = MOTION_MODEL, widget=forms.Select(attrs={'class':'form-control'}))
    number_of_iterations = forms.DecimalField(label='Iterations',
                            required=False,
                            max_digits=5,
                            decimal_places=0,
                            max_value=99000,
                            min_value=1000,
                            widget=forms.NumberInput(attrs={'size': '9', 'placeholder':'0', 'step':'1000' ,'class':'form-control'}))

    def clean_number_of_iterations(self):
        return int(self.cleaned_data['number_of_iterations'])

    def clean_warp_mode(self):
        return int(self.cleaned_data['warp_mode'])

def null_to_zero(value):
    if not value:
        return 0
    else:
        return int(value)

class LedsControlsForm(forms.ModelForm):
        class Meta:
            model = Leds_Db

            fields =[   'uv365_power',
                        'uv255_power',
                        'whitet_power',
                        'red',
                        'blue',
                        'green',
                        'white',
                        ]

        uv365_power = forms.DecimalField(label='365 nm',
                                            required=False,
                                            max_digits=3,
                                            decimal_places=0,
                                            max_value=255,
                                            min_value=0,
                                            widget=forms.NumberInput(attrs={'size': '9', 'type':'range','placeholder':'0', 'class':'custom-range form-control mx-2 my-1'}),
                                            )
        uv255_power = forms.DecimalField(label='265 nm',
                                            required=False,
                                            max_digits=3,
                                            decimal_places=0,
                                            max_value=255,
                                            min_value=0,
                                            widget=forms.NumberInput(attrs={'size': '9', 'type':'range','placeholder':'0', 'class':'custom-range form-control mx-2 my-1'}),
                                            )
        whitet_power = forms.DecimalField(label='White T',
                                            required=False,
                                            max_digits=3,
                                            decimal_places=0,
                                            max_value=255,
                                            min_value=0,
                                            widget=forms.NumberInput(attrs={'size': '9', 'type':'range','placeholder':'0', 'class':'custom-range form-control mx-2 my-1'}),
                                            )

        white = forms.DecimalField(label='White R',
                                            required=False,
                                            max_digits=3,
                                            decimal_places=0,
                                            max_value=255,
                                            min_value=0,
                                            widget=forms.NumberInput(attrs={'size': '9', 'type':'range','placeholder':'0', 'class':'custom-range form-control mx-2 my-1'}),
                                            )

        def clean_uv365_power(self):
            return null_to_zero(self.cleaned_data['uv365_power'])

        def clean_uv255_power(self):
            return null_to_zero(self.cleaned_data['uv255_power'])

        def clean_whitet_power(self):
            return null_to_zero(self.cleaned_data['whitet_power'])

        def clean_red(self):
            return null_to_zero(self.cleaned_data['red'])

        def clean_green(self):
            return null_to_zero(self.cleaned_data['green'])

        def clean_blue(self):
            return null_to_zero(self.cleaned_data['blue'])

        def clean_white(self):
            return null_to_zero(self.cleaned_data['white'])