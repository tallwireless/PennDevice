from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import *


def group(request, group_id=None):
    return render(request,'registration/group.tpl',{})

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
