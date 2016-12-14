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
            device['action'] = """<a href='javascript:void(null)' id='{0}-del'>Del</a>&nbsp;
            |&nbsp;<a href='javascript:void(null)'
            id='{0}-renew'>Renew</a>""".format(device['mac_address'])
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
                mdict['admin'] = 'Yes'
            data.append(mdict)

        return self.returnSuccess({
           'data': data,
           'recordsTotal': len(data),
           'draw': 1,
           'recordsFiltered': len(data)
           })
