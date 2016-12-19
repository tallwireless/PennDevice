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
        try:
            if user in self.devicegroupadmins.admins.all():
                return True
        except Exception:
            return False
        return False
    def asDict(self):
        return {
                'name': self.name,
                'personal': self.personal,
                'members': [ str(member) for member in self.members.all() ],
                'specialRole': self.specialRole,
                'devices': [ str(device) for device in self.device_set.all() ]
                }


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
    def asDict(self):
        return {
                'mac_address': self.mac_address,
                'owner': self.owner.pk,
                'added': str(self.added.date()),
                'expires': str(self.expires.date()),
                'added_by': self.added_by,
                'active': self.active,
                'description': self.description,
                }
    def remove(self,nac):
        nac.del_node(self)
        nac.reval_node(self)
        self.delete()

class DeviceGroupAdmins(models.Model):
    group = models.OneToOneField(DeviceGroup,
                on_delete=models.CASCADE)
    admins = models.ManyToManyField(User)
    def __str__(self):
        return "{} admins".format(self.group)

class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)
    def __str__(self):
        return self.key

class UserAttributes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    siteAdmin = models.BooleanField(default=False)

    def __str__(self):
        return "{0.username} Attributes".format(self.user)
