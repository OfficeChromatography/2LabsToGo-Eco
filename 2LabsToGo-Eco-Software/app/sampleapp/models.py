from django.db import models
from django.contrib.auth import get_user_model
import finecontrol.models as core_models
# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters

class SampleApplication_Db(core_models.Application_Db):
    class Meta(core_models.Application_Db.Meta):
        pass


class PlateProperties_Db(core_models.PlateProperties_Db):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                    related_name='plate_properties',
                                    null=True,
                                    on_delete=models.CASCADE,
                                    blank=True)

class ZeroPosition_Db(core_models.ZeroPosition_Db):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                    related_name='zero_properties',
                                    null=True,
                                    on_delete=models.CASCADE,
                                    blank=True)

class BandsComponents_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                                             related_name='band_components',
                                                             null=True,
                                                             on_delete=models.CASCADE,
                                                             blank=True)
    band_number = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
    product_name = models.CharField(null=True, max_length=120, blank=True)
    volume = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    type = models.CharField(null=True, max_length=120, blank=True)
    sample = models.DecimalField(decimal_places=0, max_digits=1, null=True, blank=True)
    density = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    viscosity = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    

class BandSettings_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                                                 related_name='band_settings',
                                                                 null=True,
                                                                 on_delete=models.CASCADE,
                                                                 blank=True)
    main_property = models.DecimalField(null=True,decimal_places=0, max_digits=6)
    value = models.DecimalField(null=True, decimal_places=0, max_digits=3)
    height = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    gap = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    waitTime = models.DecimalField(null=True, decimal_places=2, max_digits=5)

class MovementSettings_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                                                 related_name='movement_settings',
                                                                 null=True,
                                                                 on_delete=models.CASCADE,
                                                                 blank=True)
    motor_speed = models.DecimalField(null=True, decimal_places=0, max_digits=5)
    delta_x = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    delta_y = models.DecimalField(null=True, decimal_places=2, max_digits=5)

class PressureSettings_Db(models.Model):
    sample_application = models.ForeignKey(SampleApplication_Db,
                                                                 related_name='pressure_settings',
                                                                 null=True,
                                                                 on_delete=models.CASCADE,
                                                                 blank=True)
    pressure = models.DecimalField(null=True, decimal_places=0, max_digits=3)
    frequency = models.DecimalField(null=True, decimal_places=0, max_digits=4)
    temperature = models.DecimalField(null=True, decimal_places=0, max_digits=3, blank=True)
    nozzlediameter = models.CharField(max_length=120, default='0.05')
    rinsingPeriod = models.DecimalField(null=True, decimal_places=0, max_digits=6)
    rinsingSolvent = models.CharField(null=True, max_length=120, blank=True)

