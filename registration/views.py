from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import *


def group(request, group_id=None):
    #figure out current group
    current_user = PennUser.objects.get(pk=request.session['current_user'])
    if group_id == None:
        #we don't have a group, so we are going to use the personal group of
        #the user
        group_id = current_user.devicegroup_set.filter(name__contains=current_user.pk)[0].id
    context = {}
    context['user'] = current_user
    context['current_group'] = DeviceGroup.objects.get(pk=group_id)
    context['devices'] = context['current_group'].device_set.order_by('mac_address')
    context['groups'] = [ i for i in current_user.devicegroup_set.order_by('name') ]
    for index,group in enumerate(context['groups']):
        if group.name == current_user.pk:
            del context['groups'][index]
            context['groups'] = [group] + context['groups']
    return render(request,'registration/group.tpl',context)

def groupAction(request, group_id):
    return HttpResponse("Soon to be showing group {}".format(group_id))

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
