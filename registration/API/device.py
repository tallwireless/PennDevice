from registration.serializers import *

from registration.models import Device

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django.http import Http404

from pprint import pprint as pp

class DeviceAPI(generics.GenericAPIView):

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
   
    def authorized(self, obj, user):
        if user not in obj.owner.members.all():
            if not user.userattributes.siteAdmin:
                return False
        return True

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
            if not self.authorized(obj,request.user):
                return Reponse({
                    "error": True,
                    "err_msg": "You aren't authorized to view this device."})
                                
            self.serializer_class = DeviceDetailSerializer
            return Response(self.serializer_class(obj).data)
        else:
            groups = request.user.group_membership.all()
            rtv = []
            if 'action' in kwargs:
                print("Action: {}".format(kwargs['action']))
                if 'all' in kwargs['action']:
                    if request.user.userattributes.siteAdmin:
                        groups = DeviceGroup.objects.all()
                if 'detail' in kwargs['action']:
                    for group in groups:
                        for device in group.device_set.all():
                            rtv.append(DeviceDetailSerializer(device).data)
                    return Response(rtv)

            for group in groups:
                for device in group.device_set.all():
                    rtv.append(device.mac_address)

            return Response(sorted(rtv))

