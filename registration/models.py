from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DeviceGroup(models.Model):
    name = models.CharField(max_length=255)
    personal = models.BooleanField(default=False)
    members = models.ManyToManyField(User)
    specialRole = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def isAdmin(self,user):
        print(user)
        try:
            if user in self.devicegroupadmins_set.all()[0].admins.all():
                return True
        except Exception:
            return False
        return False

class Device(models.Model):
    mac_address = models.CharField(primary_key=True,
                    max_length=17,)
    owner = models.ForeignKey('DeviceGroup',
                    on_delete=models.CASCADE)
    added = models.DateTimeField()
    expires = models.DateTimeField()
    added_by = models.CharField(max_length=255)
    active = models.BooleanField(default=True)    
    description = models.CharField(max_length=255,default="")
    def __str__(self):
        return self.mac_address

class DeviceGroupAdmins(models.Model):
    group = models.ForeignKey(DeviceGroup,
                on_delete=models.CASCADE)
    admins = models.ManyToManyField(User)
    def __str__(self):
        return "{} admins".format(self.group)

class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)
    def __str__(self):
        return self.key
