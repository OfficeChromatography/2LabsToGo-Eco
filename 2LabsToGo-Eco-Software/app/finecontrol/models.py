from django.db import models
from django.contrib.auth import get_user_model

SYRINGE_VOLUME = [('3', '2 ml'),
                ('6', '5 ml'),
                ('12', '10 ml')]

SYRINGE_LENGTH = [('40', '40 mm'),
                ('50', '50 mm'),
                ('60', '60 mm')]


class GcodeFile(models.Model):
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    gcode = models.FileField(null=True)
    gcode_url = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

class CleaningProcess_Db(models.Model):
    user = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    start_frequency = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    stop_frequency = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    steps = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    pressure = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    times = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    
class SyringeLoad_Db(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    volume = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

class SyringeConfiguration(models.Model):
    volume_type = models.CharField(max_length=255, choices=SYRINGE_VOLUME, default=SYRINGE_VOLUME[0], null=True, blank=False)
    length_type = models.CharField(max_length=255, choices=SYRINGE_LENGTH, default=SYRINGE_LENGTH[0], null=True, blank=False)
    def __str__(self):
        return f"Syringe Configuration: Volume={self.SYRINGE_VOLUME}"

class ZeroPosition(models.Model):
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    zero_x = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    zero_y = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)


class ZeroPosition_Db(models.Model):
    zero_x = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    zero_y = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        abstract = True


class PlateProperties_Db(models.Model):
    size_x = models.DecimalField(decimal_places=0, max_digits=3, null=True)
    size_y = models.DecimalField(decimal_places=0, max_digits=3, null=True)
    offset_left = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_right = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    offset_bottom = models.DecimalField(decimal_places=2, max_digits=5, null=True)    

    class Meta:
        abstract = True

class Method_Db(models.Model):
    auth = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    filename = models.CharField(null=True, max_length=120)

class Application_Db(models.Model):
    auth = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    filename = models.CharField(null=True, max_length=120)
    method = models.ForeignKey(Method_Db, on_delete = models.CASCADE, null=True, blank=True)
    class Meta:
        abstract = True

class AirSensor_Db(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    temperature = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    humidity = models.DecimalField(null=True, max_digits=5, decimal_places=2)
