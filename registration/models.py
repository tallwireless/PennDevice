from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.


class DeviceGroup(models.Model):
    name = models.CharField(max_length=255)
    personal = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name="group_membership")
    specialRole = models.BooleanField(default=False)
    admins = models.ManyToManyField(User, related_name="group_admin", blank=True)
    def __str__(self):
        return self.name
    def isAdmin(self,user):
        try:
            if type(user) == str:
                user = User.objects.get(username=user)
            if user in self.admins.all():
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
                    max_length=17,
                    validators=[
                        RegexValidator(regex=r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}',
                                       message="Please enter a valid MAC Address")
                        ])
    owner = models.ForeignKey('DeviceGroup',
                    on_delete=models.CASCADE, null=True)
    added = models.DateTimeField()
    expires = models.DateTimeField(null=True)
    added_by = models.CharField(max_length=255,null=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=255,default="", null=True)
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

class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)
    def __str__(self):
        return self.key

class UserAttributes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    siteAdmin = models.BooleanField(default=False)

    def __str__(self):
        return "{0.username} Attributes".format(self.user)
