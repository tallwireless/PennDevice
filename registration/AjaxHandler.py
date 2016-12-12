from pprint import pprint as pp
from .models import *

from django.template import loader

class AjaxHandler(object):
    
    def returnError(self, mesg):
        return {'error': True, 'err_msg': mesg}
    
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

    def admin_group(self, request):
        return self.returnSuccess({'content': "YOU HAVE THE POWER!"})
        
