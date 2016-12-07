from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(DeviceGroup)
admin.site.register(Device)
admin.site.register(DeviceGroupAdmins)
admin.site.register(Setting)
