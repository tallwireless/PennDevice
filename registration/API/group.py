from registration.models import DeviceGroup
from registration.serializers import *

from rest_framework import generics, mixins
from rest_framework.response import Response

from django.http import Http404

class DeviceGroupAPI(generics.GenericAPIView):

    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    
    def get_object(self, pk):
        try:
            return DeviceGroup.objects.get(pk=pk)
        except DeviceGroup.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        #if we are given something to work with
        if 'pk' in kwargs:
            obj = self.get_object(kwargs['pk'])

            #check to see if the user is a member of the group

            print(kwargs)
            if 'action' in kwargs:
                if kwargs['action'] == 'members':
                    return Response(UserDetailSerializer(obj.members.all(), many=True).data)
                if kwargs['action'] == 'admins':
                    return Response(UserDetailSerializer(obj.admins.all(), many=True).data)
                if kwargs['action'] == 'devices':
                    return Response(DeviceDetailSerializer(obj.device_set.all(), many=True).data)
                if kwargs['action'] == 'detail':
                    self.serializer_class = DeviceGroupDetailSerializer

            if request.user not in obj.members.all():
                if not request.user.userattributes.siteAdmin:
                    return Response({'error':True,
                                     'err_msg': "You aren't a member of the group."}, 
                                     status=status.HTTP_400_BAD_REQUEST)

            return Response(self.serializer_class(obj).data)
        else:
            groups = request.user.group_membership.order_by('-name')
            rtv = []
            if 'action' in kwargs:
                if kwargs['action'] == 'all':
                    if request.user.userattributes.siteAdmin:
                        groups=DeviceGroup.objects.order_by('-name')

            for group in groups:
                print(rtv)
                print('/n')
                tmp = {'name': group.name,
                       'id'  : group.id}
                if group.personal and group.name == request.user.username:
                    rtv.insert(0,tmp)
                else:
                    rtv.append(tmp)

            return Response(rtv)
