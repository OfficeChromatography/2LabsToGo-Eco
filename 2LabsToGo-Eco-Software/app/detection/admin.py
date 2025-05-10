from django.contrib import admin
from .models import *
from django.db import models


admin.site.register(Images_Db)
admin.site.register(Detection_ZeroPosition)
admin.site.register(UserControls_Db)
admin.site.register(Leds_Db)
admin.site.register(CameraControls_Db)

