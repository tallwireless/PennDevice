from rest_framework import serializers

from .models import *
from django.contrib.auth.models import User
from pprint import pprint as pp

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id', 'first_name', 'last_name', 'email')

class UserSerializer(UserDetailSerializer):
    def to_representation(self, obj):
        return obj.username

class DeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
    def to_representation(self, obj):
         rv = super(serializers.ModelSerializer, self).to_representation(obj)
         pp(rv)
         return rv


class DeviceSerializer(DeviceDetailSerializer):
    def to_representation(self, obj):
        return obj.mac_address

class DeviceTableSerializer(DeviceDetailSerializer):
    def to_representation(self, obj):
        rv = super(DeviceDetailSerializer, self).to_representation(obj)
        rv['DT_RowId']=rv['mac_address']
        return rv
        
class DeviceGroupDetailSerializer(serializers.ModelSerializer):
    members = UserDetailSerializer(many=True)
    admins = UserDetailSerializer(many=True)
    device_set = DeviceDetailSerializer(many=True)
    class Meta:
        model = DeviceGroup
        fields = ( 'name', 'id', 'members', 'device_set', 'personal',
                'specialRole', 'admins')
        depth=1

class DeviceGroupSerializer(DeviceGroupDetailSerializer):
    members = UserSerializer(many=True)
    admins = UserSerializer(many=True)
    device_set = DeviceSerializer(many=True)
    
