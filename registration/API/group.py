from registration.models import DeviceGroup
from registration.serializers import *
from rest_framework.parsers import JSONParser

from rest_framework import generics, mixins
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.http import Http404

import json

from registration.PacketFence import PacketFence

from datetime import datetime
from datetime import timedelta

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

            table = self.request.query_params.get('table',None)

            if request.user not in obj.members.all():
                if not request.user.userattributes.siteAdmin:
                    return Response({'error':True,
                                     'err_msg': "You aren't a member of the group."}, 
                                     status=status.HTTP_400_BAD_REQUEST)
            
            if 'action' in kwargs:
                if kwargs['action'] == 'members':
                    rv = UserTableSerializer(obj.members.all(), many=True).data
                    for user in rv:
                        if obj.isAdmin(user['username']):
                            user['admin'] = True
                        else:
                            user['admin'] = False
                    if (table != None):
                        return Response({'data':rv})
                    else:
                        return Response(rv)
                if kwargs['action'] == 'devices':
                    if table != None:
                        return Response({'data':DeviceTableSerializer(obj.device_set.all(), many=True).data})
                    else:
                        return Response(DeviceDetailSerializer(obj.device_set.all(), many=True).data)
                if kwargs['action'] == 'detail':
                    self.serializer_class = DeviceGroupDetailSerializer


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

    def patch(self, request, **kwargs):
        if 'pk' in kwargs:
            obj = self.get_object(kwargs['pk'])

            table = self.request.query_params.get('table',None)

            if request.user not in obj.admins.all():
                if not request.user.userattributes.siteAdmin:
                    return Response({'error':True,
                                     'err_msg': "You aren't an admin member of the group."}, 
                                     status=status.HTTP_400_BAD_REQUEST)
            request_data = str(request.read().decode("utf-8"))
            if kwargs['action'] == 'members':
                patch_entries = json.loads(request_data)
                rv = []
                for entry in patch_entries:
                    try:
                        user = obj.members.get(username=entry['username'])
                    except Exception:
                        rv.append({'error':True, 'err-msg': "Unable to get user",'request':entry})
                    else:

                        if 'admin' in entry:
                            if entry['admin'] and not obj.isAdmin(user):
                                obj.admins.add(user)
                            elif not entry['admin'] and obj.isAdmin(user):
                                obj.admins.remove(user)
                        rv.append({'username':user.username,'admin':obj.isAdmin(user)})
                return Response(rv)
            return Response({})
    def delete(self, request, **kwargs): 
        if 'pk' in kwargs:
            obj = self.get_object(kwargs['pk'])

            table = self.request.query_params.get('table',None)

            if request.user not in obj.admins.all():
                if not request.user.userattributes.siteAdmin:
                    return Response({'error':True,
                                     'err_msg': "You aren't an admin member of the group."}, 
                                     status=status.HTTP_400_BAD_REQUEST)
            
            if kwargs['action'] == 'members':
                if 'item' in kwargs:
                    try:
                        user = obj.members.get(username=kwargs['item'])
                    except Exception:
                        return Response({"error":True, 
                                         "err-msg": "Please provide a user that is a member of the group."})
                    else:
                        if obj.isAdmin(user):
                            obj.admins.remove(user)
                        obj.members.remove(user)
                        return Response({"error": False,
                                         "username": user.username})


    def put(self, request, **kwargs):
        """This is to handle adding things to a group. Things that are
        supported include devices and members."""

        #Check to make sure that we have a group number
        if 'pk' not in kwargs:
            raise Http404
        #Fetch the group 
        group = self.get_object(kwargs['pk'])
        
        #are we dealing with a table?
        table = self.request.query_params.get('table',None)

        #let's see what data is out there
        request_data = json.loads(str(request.read().decode("utf-8")))
        
        #dealing with devices
        if kwargs['action'] == 'devices':
            
            #Some basic permissions checking
            if request.user not in group.members.all():
                if not request.user.userattributes.siteAdmin:
                    return Response({'error':True,
                                     'err_msg': "You aren't a member of the group."}, 
                                     status=status.HTTP_400_BAD_REQUEST)
            
            nac = PacketFence()

            # how long should the device exist for in the system before being
            # removed
            expires_count = 0
            if group.personal:
                expires_count = int(Setting.objects.get(pk='personal.default.expire_length').value)
            else:
                expires_count = int(Setting.objects.get(pk='group.default.expire_length').value)

            #dealing with a single item
            if 'item' in kwargs:
                mac = kwargs['item'].lower()
                des = ""
                
                #trim the description to fit in the field
                if 'des' in request_data:
                    if len(request_data['des']) > 255:
                        des = request_data['des'][0:255]
                    else:
                        des = request_data['des']
                
                try:
                    #Let's add it to the database
                    pp(mac)
                    d = Device.objects.create(
                        mac_address = mac,
                        owner = group,
                        added_by = request.user.username,
                        added = datetime.utcnow(),
                        expires = datetime.utcnow()+timedelta(days=expires_count),
                        description = des,
                    )
                    #and add it to the NAC
                    nac.add_node(d,group)
                    nac.reval_node(d)
                except IntegrityError as err:
                    return Response({'error':True,
                        'err_msg': "This MAC address has already been registered"})
                except ValidationErr as err:
                    return Response({'error':True,
                        'err_msg': "Please provide a properly formated MAC address"})
                except Exception as err:
                    return Response({'error': True,
                        'err_msg': "There was an error adding the device."})

                else:
                    return Response(DeviceTableSerializer(d).data)

                        
