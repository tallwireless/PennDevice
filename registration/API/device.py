from registration.serializers import *

from registration.models import Device

from rest_framework import generics, mixins
from rest_framework.response import Response

from django.http import Http404

class DeviceAPI(generics.GenericAPIView):

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
    def get_object(self, mac):
        try:
            return Device.objects.get(mac_address=mac)
        except DeviceGroup.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        #if we are given something to work with
        if 'mac' in kwargs:
            obj = self.get_object(kwargs['mac'])

            #check to see if the user is a member of the group

            self.serializer_class = DeviceDetailSerializer
            return Response(self.serializer_class(obj).data)
        else:
            devices = Device.objects.order_by('mac_address')
            rtv = [ device.mac_address for device in devices ]
            return Response(rtv)
