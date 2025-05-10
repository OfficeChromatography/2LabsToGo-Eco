from django.db import models
from django.contrib.auth import get_user_model
import os

from finecontrol.models import Method_Db

AWB_MODES = [('0', 'off'),
            ('1', 'auto'),
            ('2', 'tungsten'),
            ('3', 'fluorescent'),
            ('4', 'indoor'),
            ('5', 'daylight'),
            ('6', 'cloudy'),
            ('7', 'custom')]

AUTO_EXPOSURE = [('0', 'off'),
                ('1', 'on')]

FORMATS = (('0','BMP'),    
            ('1','PNG'),
            ('2','JPEG'))

class PlatePhoto_Db(models.Model):
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to='media/')

class CameraControls_Db(models.Model):
    auto_exposure = models.CharField(max_length=255, choices=AUTO_EXPOSURE, default=AUTO_EXPOSURE[0], null=True, blank=False)

    exposure_time_absolute = models.DecimalField(
                            null=True,
                            blank=False,
                            default=0.025,
                            max_digits=7,
                            decimal_places=4)

    white_balance_auto_preset = models.CharField(max_length=255, choices=AWB_MODES,
                                                 default=AWB_MODES[0], null=True, blank=False)

    analogue_gain = models.DecimalField(
                            null=True,
                            blank=False,
                            default=None,
                            max_digits=3,
                            decimal_places=1)

    colour_gains = models.CharField(max_length=10, default='1.0,1.0', null=True, blank=False)

    imagenumber = models.DecimalField(
                            null=True,
                            blank=False,
                            default=1,
                            max_digits=3,
                            decimal_places=0)

    delaytime = models.DecimalField(
                            null=True,
                            blank=False,
                            default=0,
                            max_digits=3,
                            decimal_places=0)

class UserControls_Db(models.Model):

    brightness =    models.DecimalField(
                        null=True,
                        blank=True,
                        default=0,
                        max_digits=2,
                        decimal_places=1)

    contrast =     models.DecimalField(
                        null=True,
                        blank=True,
                        default=1,
                        max_digits=3,
                        decimal_places=1)

    saturation =     models.DecimalField(
                        null=True,
                        blank=True,
                        default=1,
                        max_digits=3,
                        decimal_places=1)

    sharpness = models.DecimalField(
                        null=True,
                        blank=True,
                        default=1,
                        max_digits=3,
                        decimal_places=1)

class Leds_Db(models.Model):
    uv365_power = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

    uv255_power = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

    whitet_power = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)  

    red = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

    blue = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

    green = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

    white = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=0)

class Images(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    note = models.TextField(default="", null=True, blank=True)

class Images_Db(Images):
    image = models.ImageField(upload_to ='images/', default='/default.jpg')
    leds_conf   = models.OneToOneField(Leds_Db, on_delete=models.CASCADE, null=True, blank=True)
    camera_conf = models.OneToOneField(CameraControls_Db, on_delete=models.CASCADE, null=True, blank=True)
    user_conf   = models.OneToOneField(UserControls_Db, on_delete=models.CASCADE, null=True, blank=True)

    method = models.ForeignKey(Method_Db, on_delete = models.CASCADE, null=True, blank=True)

    def file_name(self):
        return os.path.splitext(os.path.basename(self.image.name))[0]

    def delete(self, *args, **kwargs):
        self.user_conf.delete()
        self.leds_conf.delete()
        self.camera_conf.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Detection_ZeroPosition(models.Model):
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    zero_x = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    zero_y = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)