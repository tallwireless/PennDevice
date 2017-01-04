from pprint import pprint as pp
from .models import *

from django.template import loader

from .PacketFence import PacketFence

from datetime import datetime,timedelta

def is_vaild_mac_address(str):
    return True

class AjaxHandler(object):

    def returnError(self, mesg, data={}):
        data['error'] = True
        data['err_msg'] = mesg
        return data
    
    def returnSuccess(self, data):
        data['error'] = False
        return data

    def handle(self, request):
        if not request.is_ajax():
            return self.returnError('This isn\'t AJAX.')

        func = ""
        try:
            func = request.POST['func']
        except Exception:
            return self.returnError('Function Not given')
        
        func_call = getattr(self, func, None)
        if func_call == None:
            return self.returnError('Funciton "'+func+'" not defined')

        return func_call(request)


    def add_devices_form(self, request):
        group = None
        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))
        context = {}
        if group.personal:
            context['available_device_count'] = int(Setting.objects.get(pk='personal.max_count').value)-len(group.device_set.all())
        else:
            context['available_device_count'] = int(Setting.objects.get(pk='group.max_count').value) - len(group.device_set.all())
        context['num_add_fields'] = range(min(
                context['available_device_count'],
                int(Setting.objects.get(pk='general.add_count').value)
                ))
        context['current_group']= group
        template = loader.get_template('registration/forms/add_device.tpl')
        return self.returnSuccess(
                {'content': template.render(context,request), 
                    'resource': 'add_device'})

    def updateDevice(self, request):
        user = request.user
        group = device =  None
        func = ""
        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
            device = Device.objects.get(pk=request.POST['device'])
        except Exception as e:
            return self.returnError("There was an error updating your device.")

        try:
            func = request.POST['updateAction']
        except Exception:
            return self.returnError("No update action given")

        if( func == "del" ):
            # do some deleting here
            data = {
                    'device': device.pk,
                    'group_id': group.id,
                    'updateAction': 'del',
                    }
            try: 
                device.remove(PacketFence())
            except Exception as e:
                data['exception'] = str(e)
                return self.returnError("Unable to delete device", data)
            else:
                return self.returnSuccess(data)

        elif( func == "renew" ):

            return self.returnError("This hasn't been developed yet.")

        return self.returnError("Invalid device update action")
        

    def admin_group(self, request):
        user = request.user
        group = None
       
        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))
        
        if not group.isAdmin(user):
            return self.returnError("You are not an admin of the {} group.".format(group.name))

        members = []
        for member in group.members.order_by('last_name'):
            members.append( { 'name': "{} {}".format(member.first_name,member.last_name),
                              'username': member.username,
                              'group_admin': group.isAdmin(member)
                              } )
        context={}
        context['members'] = members
        template = loader.get_template('registration/forms/admin_group.tpl')
        return self.returnSuccess({'content':
            template.render(context,request), 'resource': 'admin_group' })
        
    def add_device(self,request):
        user = request.user
        group = None
        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))

        if user not in group.members.all():
            return self.returnError("Not a member of the group "+group.name+".")

        data = {}
        for key in request.POST:
            if 'data' in key:
                if 'name' in key:
                    f = request.POST[key].split('-')
                    v = request.POST[key.replace("name","value")]
                    if f[1] not in data:
                        data[f[1]] = {'err': False, 'empty': False}
                    data[f[1]][f[0]]=v

        for i in data:
            if data[i]['mac'] == "":
                data[i]['empty'] = True;
                continue
            if not is_vaild_mac_address(data[i]['mac']):
                data[i]['err']=True
                data[i]['err_msg'] = 'Invalid formatted MAC Address'
                continue

            try:
                pf = PacketFence()
                expires_count = 0
                if group.personal:
                    expires_count = int(Setting.objects.get(pk='personal.default.expire_length').value)
                else:
                    expires_count = int(Setting.objects.get(pk='group.default.expire_length').value)
                d = Device.objects.create(
                        mac_address = data[i]['mac'].lower(),
                        owner = group,
                        added_by = user.username,
                        added = datetime.utcnow(),
                        expires = datetime.utcnow()+timedelta(days=expires_count),
                        description = data[i]['des']
                )
                pf.add_node(d,group)
                pf.reval_node(d)
            except Exception as e:
                data[i]['err']=True
                data[i]['err_msg']="There was an issue adding the device."

        return self.returnSuccess({'data': data})

    def get_device(self, request):
        user = request.user
        group = None
        
        device = None
        
        try:
            device = Device.objects.get(pk=request.POST['device'])
        except Exception:
            return self.returnError("Error getting requested device")

        if user not in device.owner.members.all():
            return self.returnError("You don't own this device.")

        return self.returnSuccess({'device': device.asDict()})

    def get_group_device_table(self,request):
        user = request.user
        group = None

        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))

        if user not in group.members.all():
            return self.returnError("Not a member of the group "+group.name+".")
        
        totalDevices = len(group.device_set.all())
        
        rdata = []
        for device in group.device_set.order_by('mac_address'):
            device = device.asDict()
            device['DT_RowId'] = device['mac_address']
            rdata.append(device)
        return self.returnSuccess({
                'data':rdata, 
                'recordsTotal': totalDevices,
                'draw': 1,
                'recordsFiltered': len(rdata),
                })

    def get_group_members_table(self,request):
        user = request.user
        group = None

        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))

        if user not in group.members.all():
            return self.returnError("Not a member of the group "+group.name+".")
        if not group.isAdmin(user):
            return self.returnError("You aren't a admin of group "+group.name+".")

        data = []
        for member in group.members.order_by('last_name'):
            mdict = {}
            mdict['fname'] = member.first_name
            mdict['lname'] = member.last_name
            mdict['username'] = member.username
            mdict['DT_RowId'] = mdict['username']
            if group.isAdmin(member):
                mdict['admin'] = 'Yes'
            else:
                mdict['admin'] = 'No'
            data.append(mdict)

        return self.returnSuccess({
           'data': data,
           'recordsTotal': len(data),
           'draw': 1,
           'recordsFiltered': len(data)
           })

    def updateGroupMember(self,request):
        user = request.user
        group = None
        
        try:
            group = DeviceGroup.objects.get(pk=request.POST['group_id'])
        except Exception as e:
            return self.returnError("There is no group defined for the session."+str(e))

        if user not in group.members.all():
            return self.returnError("Not a member of the group "+group.name+".")
        if not group.isAdmin(user):
            return self.returnError("You aren't a admin of group "+group.name+".")
        
        requiredFields = [ 'updateAction', 'user' ]

        for field in requiredFields:
            if field not in request.POST:
                return self.returnError("Required field {} not found".format(field))
        
        action = request.POST['updateAction']


        if action == 'addMember':
            newUser = None
            try:
                newUser = User.objects.get(username=request.POST['user'])
            except Exception as e:
                # user hasn't logged in yet
                newUser = User.objects.create(username=request.POST['user'])

            if newUser in group.members.all():
                return self.returnError("The user {0.username} is already a member of the group {1}".format(newUser,group))

            group.members.add(newUser)
            return self.returnSuccess({
                'sucMsg': "{0.first_name} {0.last_name} ({0.username}) has been added to the group {1}".format(newUser,group),
                'member': {
                    'DT_RowId': newUser.username,
                    'fname': newUser.first_name,
                    'lname': newUser.last_name,
                    'username': newUser.username,
                    'admin': 'No'
                    },
                'action': 'addMember',
                })


        try:
            actionUser = User.objects.get(username=request.POST['user'])
        except Exception as e:
            return self.returnError("User doesn't exist")
        if user == actionUser:
            return self.returnError("You can't modify your own account.")

        if action == 'del':
            try:
                if group.isAdmin(actionUser):
                    group.admins.remove(actionUser)
                group.members.remove(actionUser)
            except Exception as e:
                pp(e)
                return self.returnError("Unable to remove {} from the {} group".format(actionUser, group))

            return self.returnSuccess({
                'action':'del', 
                'user': actionUser.username,
                'sucMsg': "{0.first_name} {0.last_name} ({0.username}) has been removed from the group {1}".format(actionUser,group),
                })
        elif action == 'toggle':
            try:
                grpAdm = group.admins
                data = {
                        'action': 'toggle',
                        'user': actionUser.username,
                        'admin': "",
                        }
                if group.isAdmin(actionUser):
                    grpAdm.remove(actionUser)
                    data['admin']='No'
                    data['sucMsg'] = "{0.first_name} {0.last_name} ({0.username}) is no longer an administrator of {1}".format(actionUser,group)
                    return self.returnSuccess(data)
                else:
                    grpAdm.add(actionUser)
                    data['admin']='Yes'
                    data['sucMsg'] = "{0.first_name} {0.last_name} ({0.username}) is now an administrator of {1}".format(actionUser,group)
                    return self.returnSuccess(data)
            except Exception as e:
                print(e)
                return self.returnError("Unable to remove {} as admin from the {} group".format(actionUser,group))

        return self.returnError("updateAction {} is invalid")

    def admin(self,request):
        if 'page' in request.POST:
            if request.POST['page'] == 'groups':
                context = {}
                context['groups'] = [ i for i in DeviceGroup.objects.order_by('name') ]
                template = loader.get_template('registration/admin/group.tpl')
                return self.returnSuccess(
                        {'content': template.render(context,request), 
                            'page': 'groups'})
            
            return self.returnSuccess(
                    {'content': "this is a holder page",
                        'page': request.POST['page']})
