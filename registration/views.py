from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from pprint import pprint as pp

from datetime import datetime,timedelta

from .models import *

class DeviceFormLine():
    err_msg = ""
    error = False
    mac = ""
    desc = ""
    index = -1
    def __str__(self):
        return "index: {}\nerror: {} \nerr_msg: {} \nmac: {}\ndesc: {}".format(self.index, self.error, self.err_msg, self.mac, self.desc)

def is_valid_mac(mac):
    return True

def group(request, group_id=None, get_info=None):
    #figure out current group
    current_user = PennUser.objects.get(pk=request.session['current_user'])
    if group_id == None:
        #we don't have a group, so we are going to use the personal group of
        #the user
        group_id = current_user.devicegroup_set.filter(name__contains=current_user.pk)[0].id
    context = {}
    if get_info is not None:
        context['get_info']=get_info
    context['user'] = current_user
    context['current_group'] = DeviceGroup.objects.get(pk=group_id)
    context['devices'] = context['current_group'].device_set.order_by('mac_address')
    context['groups'] = [ i for i in current_user.devicegroup_set.order_by('name') ]
    for index,group in enumerate(context['groups']):
        if group.name == current_user.pk:
            del context['groups'][index]
            context['groups'] = [group] + context['groups']
    if context['current_group'].personal:
        context['available_device_count'] = int(Setting.objects.get(pk='personal.max_count').value) - len(context['devices'])
    else:
        context['available_device_count'] = int(Setting.objects.get(pk='group.max_count').value) - len(context['devices'])
    context['num_add_fields'] = range(min(
            context['available_device_count'],
            int(Setting.objects.get(pk='general.add_count').value)
            ))
    return render(request,'registration/group.tpl',context)

def groupActionAdd(request, group_id=None):
    get_info = {}
    error = False
    for key in request.POST:
        if key == "csrfmiddlewaretoken":
            continue
        key = key.split('-')
        if key[1] not in get_info:
            get_info[key[1]] = DeviceFormLine() 
            get_info[key[1]].index = key[1]
        if key[0] == 'desc':
            get_info[key[1]].desc = request.POST["-".join(key)]
        if key[0] == 'mac':
            get_info[key[1]].mac = request.POST["-".join(key)]
        
    try:
        grp = DeviceGroup.objects.get(pk=group_id)
    except Exception:
        print("FIRE FIRE FIRE")
        #Something went horribly wrong!
    else:
        #iterate over the get_info and deal with it
        user = PennUser.objects.get(pk=request.session['current_user'])
        print("I'm Here!")
        for k in get_info:
            pp(get_info[k])
            if get_info[k].mac == "":
                continue
            if not is_valid_mac(get_info[k].mac):
                print("fail3")
                get_info[k].error=error=True
                get_info[k].err_msg="not vaild mac address"
                continue
            else:
                if len(get_info[k].desc) > 255:
                    get_info[k].desc = get_info[k].desc[:255]
            #Let's try to put it into the database
            try:
                print("shoving in")
                expires_count = 0
                if grp.personal:
                    expires_count = int(Setting.objects.get(pk='personal.default.expire_length').value)
                else:
                    expires_count = int(Setting.objects.get(pk='group.default.expire_length').vaule)

                d = Device.objects.create(
                        mac_address = get_info[k].mac.lower(),
                        owner = grp,
                        added_by = user.pk,
                        added = datetime.utcnow(),
                        expires = datetime.utcnow()+timedelta(days=expires_count),
                        description = get_info[k].desc
                )
                print(d)
            except Exception as e:
                print(e)
                get_info[k].error=error=True
                get_info[k].err_msg="Issue adding to the database"
    if error:
        return group(request, group_id, get_info)
    return HttpResponseRedirect(reverse('reg:group',args=[group_id]))

def swapUser(request):
    try:
        currentUser = request.session['current_user']
    except KeyError:
        currentUser = 'charlesr'
    context = {
            'user': currentUser,
            'user_list': PennUser.objects.order_by('pennkey'),
        }
    return render(request, 'registration/swapUser.tpl', context)

def swapUserAction(request):
    try:
        new_user = PennUser.objects.get(pk=request.POST['new_user'])
    except (KeyError, PennUser.DoesNotExist):
        return render( request, 'registration/swapUser.tpl', 
                { 
                    'user': request.session['current_user'], 
                    'user_list': PennUser.objects.order_by('pennkey'), 
                    'error_message': "Something went wrong"
                }
            )
    else:
        request.session['current_user'] = new_user.pennkey

        return HttpResponseRedirect(reverse('reg:swapUser'))
