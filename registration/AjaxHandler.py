from pprint import pprint as pp
from .models import *

from django.template import loader

from .PacketFence import PacketFence

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
        return self.returnSuccess({'content': template.render(context,request)})

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
            return self.returnSuccess(data)

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
        for member in group.members.all():
            members.append( { 'name': "{} {}".format(member.first_name,member.last_name),
                              'username': member.username,
                              'group_admin': group.isAdmin(member)
                              } )
        context={}
        context['members'] = members
        template = loader.get_template('registration/forms/admin_group.tpl')
        return self.returnSuccess({'content': template.render(context,request) })
        
