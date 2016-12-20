from registration.serializers import *

from django.contrib.auth.models import User

from rest_framework import generics, mixins
from rest_framework.response import Response

from django.http import Http404

class UserAPI(generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self, un):
        try:
            print(un)
            return User.objects.get(username=un)
        except DeviceGroup.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        #if we are given something to work with
        if 'username' in kwargs:
            obj = self.get_object(kwargs['username'])

            #check to see if the user is a member of the group

            self.serializer_class = UserDetailSerializer
            if 'action' in kwargs:
                if kwargs['action'] == 'groups':
                    if request.user.userattributes.siteAdmin:
                        
                        return Response([{'name': g.name, 'id':g.id} for g in obj.group_membership.all()])
                    else:
                        return Response({'error':True, 'err_msg':"You aren't a site admin."})
            return Response(self.serializer_class(obj).data)
        else:
            users = User.objects.order_by('username')
            rtv = [ user.username for user in users ]
            return Response(rtv)
