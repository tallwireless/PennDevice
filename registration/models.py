from django.db import models

# Create your models here.


class PennUser(models.Model):
    pennkey = models.CharField(max_length=255)
    lastLogin = models.DateTimeField(auto_now=True)
    siteAdmin = models.BooleanField(default=True)
    def __str__(self):
        return self.pennkey

class DeviceGroup(models.Model):
    name = models.CharField(max_length=255)
    personal = models.BooleanField(default=True)
    members = models.ManyToManyField(PennUser)
    def __str__(self):
        return self.name

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
    admins = models.ManyToManyField(PennUser)
    def __str__(self):
        return "{} admins".format(self.group)
