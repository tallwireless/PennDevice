from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from pprint import pprint as pp

import logging

from datetime import datetime,timedelta

from .models import *
from .PacketFence import PacketFence
from .AjaxHandler import AjaxHandler

log = logging.getLogger('django')

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

@login_required
def group(request, group_id=None, get_info=None):
    #figure out current group
    current_user = request.user
    if group_id == None:
        #we don't have a group, so we are going to use the personal group of
        #the user
        group_id = current_user.group_membership.filter(name__contains=current_user.username)
        log.debug("group_id: {}".format(group_id))
        if len(group_id) == 0:
            grp = DeviceGroup.objects.filter(name__contains=current_user.username)
            log.debug("grp: {}".format(grp))
            if len(grp) == 1:
                log.debug("all ready have a group id")
                group_id=grp[0].id
            else:
                log.debug("Creating group for {}".format(current_user))
                grp = DeviceGroup.objects.create(
                        name = current_user.username,
                        personal = True,
                    )
                grp.members.add(current_user)
                grp.save()
                group_id = grp.id
                log.debug("My group id is now {}".format(group_id))
        else:
            group_id = group_id[0].id
    log.debug("My group id is now {}".format(group_id))
    context = {}
    if get_info is not None:
        context['get_info']=get_info
    context['user'] = current_user
    context['current_group'] = DeviceGroup.objects.get(pk=group_id)
    context['devices'] = context['current_group'].device_set.order_by('mac_address')
    context['groups'] = [ i for i in current_user.group_membership.order_by('name') ]
    context['is_admin'] = context['current_group'].isAdmin(current_user)
    try:
        context['site_admin'] = current_user.userattributes.siteAdmin
    except Exception:
        ua = UserAttributes(user_id=current_user.id)
        ua.save()
        context['site_admin'] = current_user.userattributes.siteAdmin
    if not context['current_group'].personal:
        admins = context['current_group'].admins.order_by('last_name')
        if not len(admins) == 0:
            context['admin_str'] = ""
            for (i,admin) in enumerate(admins):
                if i==len(admins)-1 and i!=0:
                    context['admin_str'] += ', and '  
                elif i!=0:
                    context['admin_str'] += ', '
                context['admin_str'] += "{} {}".format(
                        admin.first_name,
                        admin.last_name )
    for index,group in enumerate(context['groups']):
        if group.name == current_user.username:
            del context['groups'][index]
            context['groups'] = [group] + context['groups']
    request.session['gid'] = group_id
    rtn = render(request,'registration/group.tpl',context)
    rtn.set_cookie('gid',group_id)
    return rtn


def ajaxHandler(request): 
    handler = AjaxHandler()
    f = handler.handle(request)
    return JsonResponse(f)

@login_required
def admin(request):
    context = {}
    try:
        context['site_admin'] = request.user.userattributes.siteAdmin
    except Exception:
        ua = UserAttributes(user_id=request.user.id)
        ua.save()
        context['site_admin'] = request.user.userattributes.siteAdmin
    rtn = render(request,'registration/admin.tpl',context)
    return rtn
