from registration.serializers import *

from registration.models import Device

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django.http import Http404,HttpResponse

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

    def patch(self, request, **kwargs):
        # If we don't have a MAC address
        if 'mac' not in kwargs:
            return self.get(request, **kwargs)

        device = self.get_object(kwargs['mac'])
       
        if not self.authorized(device,request.user):
            return Response({"error": True,
                             "err_msg": "You aren't a member of the owning group."
                         })

        fields = JSONParser().parse(request)

        for field in fields:
            if field == 'active':
                if request.user.userattributes.siteAdmin:
                    if type(fields[field]) == bool:
                        device.active = fields[field]
            elif field == 'description':
                if len(fields[field]) > 255:
                    fields[field] = fields[field][0:254]
                device.description = fields[field]
            elif field == 'expires':
                continue

        device.save()
        
        return Response(DeviceDetailSerializer(device).data)

    def delete(self, request, **kwargs):
        #if we don't have a mac address, just return
        if 'mac' not in kwargs:
            return self.get(request, **kwargs)
        
        ui = self.request.query_params.get('ui',None)
        device = self.get_object(kwargs['mac'])

        if not self.authorized(device, request.user):
            return Response({"error": True,
                             "err_msg": "You are not authorized to do that."
                          })

        try:
            device.delete()
        except Exception:
            return Response({"error": True,
                             "err-msg": "unable to delete device"})

        if ui is not None:
            return Response({'device':kwargs['mac'],'error':False})
        else:
            return HttpResponse(status=204)

